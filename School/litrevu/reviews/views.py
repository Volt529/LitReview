from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, TicketReviewForm
from django.contrib.auth.models import User


@login_required(login_url='login')
def home(request):
    """Page d'accueil - Flux des tickets et critiques"""
    # Récupérer les utilisateurs que je suis
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    
    # Récupérer mes posts + les posts des utilisateurs que je suis
    tickets = Ticket.objects.filter(
        user__in=list(followed_users) + [request.user.id]
    )
    reviews = Review.objects.filter(
        user__in=list(followed_users) + [request.user.id]
    )
    
    # Ajouter un attribut 'type' pour distinguer les posts
    posts = []
    for ticket in tickets:
        ticket.post_type = 'ticket'
        posts.append(ticket)
    for review in reviews:
        review.post_type = 'review'
        posts.append(review)
    
    # Trier par date
    posts.sort(key=lambda x: x.time_created, reverse=True)
    
    return render(request, 'reviews/home.html', {'posts': posts})


@login_required(login_url='login')
def create_ticket(request):
    """Créer un ticket (demande de critique)"""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, '✅ Votre ticket a été créé avec succès !')
            return redirect('home')
    else:
        form = TicketForm()

    return render(request, 'reviews/create_ticket.html', {'form': form})


@login_required(login_url='login')
def create_review(request, ticket_id):
    """Créer une critique à partir d'un ticket existant"""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Empêcher plusieurs critiques sur le même ticket par le même utilisateur
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(request, '⚠️ Vous avez déjà créé une critique pour ce ticket.')
        return redirect('home')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, '✅ Votre critique a été créée avec succès !')
            return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {
        'form': form,
        'ticket': ticket
    })


@login_required(login_url='login')
def create_ticket_review(request):
    """Créer un ticket ET une critique en même temps"""
    if request.method == 'POST':
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer le ticket
            ticket = Ticket.objects.create(
                title=form.cleaned_data['ticket_title'],
                description=form.cleaned_data['ticket_description'],
                image=form.cleaned_data['ticket_image'],
                user=request.user
            )

            # Créer la critique liée
            Review.objects.create(
                ticket=ticket,
                headline=form.cleaned_data['review_headline'],
                rating=form.cleaned_data['review_rating'],
                body=form.cleaned_data['review_body'],
                user=request.user
            )

            messages.success(request, '✅ Ticket et critique créés avec succès !')
            return redirect('home')
    else:
        form = TicketReviewForm()

    return render(request, 'reviews/create_ticket_review.html', {'form': form})


@login_required(login_url='login')
def user_posts(request):
    """Afficher uniquement les posts de l'utilisateur connecté"""
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    posts = list(tickets) + list(reviews)
    posts = []
    for ticket in tickets:
        ticket.post_type = 'ticket'
        posts.append(ticket)
    for review in reviews:
        review.post_type = 'review'
        posts.append(review)
        
    posts.sort(key=lambda x: x.time_created, reverse=True)

    return render(request, 'reviews/user_posts.html', {'posts': posts})


@login_required(login_url='login')
def subscriptions(request):
    """Page des abonnements"""
    # Les utilisateurs que je suis
    following = UserFollows.objects.filter(user=request.user).select_related('followed_user')
    
    # Les utilisateurs qui me suivent
    followers = UserFollows.objects.filter(followed_user=request.user).select_related('user')
    
    return render(request, 'reviews/subscriptions.html', {
        'following': following,
        'followers': followers
    })


@login_required(login_url='login')
def follow_user(request):
    """Suivre un utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        
        if not username:
            messages.error(request, '⚠️ Veuillez entrer un nom d\'utilisateur.')
            return redirect('subscriptions')
        
        # Vérifier que l'utilisateur existe
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'⚠️ L\'utilisateur "{username}" n\'existe pas.')
            return redirect('subscriptions')
        
        # Vérifier qu'on ne se suit pas soi-même
        if user_to_follow == request.user:
            messages.error(request, '⚠️ Vous ne pouvez pas vous suivre vous-même.')
            return redirect('subscriptions')
        
        # Vérifier qu'on ne suit pas déjà cet utilisateur
        if UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
            messages.error(request, f'⚠️ Vous suivez déjà {username}.')
            return redirect('subscriptions')
        
        # Créer l'abonnement
        UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
        messages.success(request, f'✅ Vous suivez maintenant {username} !')
        
    return redirect('subscriptions')


@login_required(login_url='login')
def unfollow_user(request, user_id):
    """Se désabonner d'un utilisateur"""
    follow = get_object_or_404(UserFollows, user=request.user, followed_user_id=user_id)
    username = follow.followed_user.username
    follow.delete()
    messages.success(request, f'✅ Vous ne suivez plus {username}.')
    return redirect('subscriptions')


@login_required(login_url='login')
def edit_ticket(request, ticket_id):
    """Modifier un ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Votre ticket a été modifié avec succès !')
            return redirect('user_posts')
    else:
        form = TicketForm(instance=ticket)
    
    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required(login_url='login')
def delete_ticket(request, ticket_id):
    """Supprimer un ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, '✅ Votre ticket a été supprimé.')
        return redirect('user_posts')
    
    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


@login_required(login_url='login')
def edit_review(request, review_id):
    """Modifier une critique"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Votre critique a été modifiée avec succès !')
            return redirect('user_posts')
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review,
        'ticket': review.ticket
    })


@login_required(login_url='login')
def delete_review(request, review_id):
    """Supprimer une critique"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, '✅ Votre critique a été supprimée.')
        return redirect('user_posts')
    
    return render(request, 'reviews/delete_review.html', {'review': review})