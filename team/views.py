from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import UserProfile, Match, Player, Attendance, GoalEvent, AssistEvent
from .forms import PlayerProfileForm, UserProfileForm, AttendanceForm
from django.shortcuts import get_object_or_404

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                return HttpResponseForbidden("User profile not found.")
            if user_profile.role != role and user_profile.role != 'admin':
                return HttpResponseForbidden("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

from django.db.models import Count, Max, F, Q, Avg

@login_required
@role_required('admin')
def dashboard(request):
    from datetime import datetime, timedelta
    
    # Get all players and matches
    players = Player.objects.all()
    matches = Match.objects.all().order_by('-datetime')
    
    # Calculate team stats
    total_matches = matches.count()
    total_players = players.count()
    total_goals = GoalEvent.objects.count()
    total_assists = AssistEvent.objects.count()
    
    # Calculate win rate
    wins = 0
    losses = 0
    draws = 0
    for match in matches:
        if match.score:
            scores = match.score.split('-')
            if len(scores) == 2:
                try:
                    team_score = int(scores[0])
                    opponent_score = int(scores[1])
                    if team_score > opponent_score:
                        wins += 1
                    elif team_score < opponent_score:
                        losses += 1
                    else:
                        draws += 1
                except ValueError:
                    pass
    
    win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
    
    # Top scorers and assisters
    top_scorers = Player.objects.filter(goals__gt=0).order_by('-goals')[:5]
    top_assisters = Player.objects.filter(assists__gt=0).order_by('-assists')[:5]
    
    # Recent matches (last 5) with parsed results
    recent_matches_list = []
    for match in matches[:5]:
        match_data = {
            'match': match,
            'result': None
        }
        if match.score:
            scores = match.score.split('-')
            if len(scores) == 2:
                try:
                    team_score = int(scores[0])
                    opponent_score = int(scores[1])
                    if team_score > opponent_score:
                        match_data['result'] = 'win'
                    elif team_score < opponent_score:
                        match_data['result'] = 'loss'
                    else:
                        match_data['result'] = 'draw'
                except ValueError:
                    pass
        recent_matches_list.append(match_data)
    
    # Chart data
    chart_data = {
        'win_rate': {
            'wins': wins,
            'losses': losses,
            'draws': draws,
        },
        'top_scorers': {
            'labels': [p.name for p in top_scorers],
            'data': [p.goals for p in top_scorers],
        },
        'top_assisters': {
            'labels': [p.name for p in top_assisters],
            'data': [p.assists for p in top_assisters],
        }
    }
    
    context = {
        'total_matches': total_matches,
        'total_players': total_players,
        'total_goals': total_goals,
        'total_assists': total_assists,
        'win_rate': round(win_rate, 1),
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'top_scorers': top_scorers,
        'top_assisters': top_assisters,
        'recent_matches': recent_matches_list,
        'chart_data': chart_data,
    }
    return render(request, 'team/dashboard.html', context)

@login_required
@role_required('admin')
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    attendances = Attendance.objects.filter(match=match).select_related('player')
    
    if request.method == 'POST':
        if 'update_score' in request.POST:
            match.score = request.POST.get('score')
            match.tactical_notes = request.POST.get('tactical_notes')
            match.save()
            return redirect('team:match_detail', match_id=match.id)
        
        elif 'update_ratings' in request.POST:
            for att in attendances:
                rating_val = request.POST.get(f'rating_{att.id}')
                if rating_val:
                    att.rating = float(rating_val)
                    att.save()
            return redirect('team:match_detail', match_id=match.id)

        elif 'add_goal' in request.POST:
            player_id = request.POST.get('player')
            minute = request.POST.get('minute')
            if player_id and minute:
                GoalEvent.objects.create(match=match, player_id=player_id, minute=minute)
            return redirect('team:match_detail', match_id=match.id)

        elif 'add_assist' in request.POST:
            player_id = request.POST.get('player')
            minute = request.POST.get('minute')
            if player_id and minute:
                AssistEvent.objects.create(match=match, player_id=player_id, minute=minute)
            return redirect('team:match_detail', match_id=match.id)

    goals = GoalEvent.objects.filter(match=match).select_related('player')
    assists = AssistEvent.objects.filter(match=match).select_related('player')
    
    # Players who are 'going' are eligible for events
    eligible_players = [att.player for att in attendances if att.status == 'going']

    context = {
        'match': match,
        'attendances': attendances,
        'goals': goals,
        'assists': assists,
        'eligible_players': eligible_players,
    }
    return render(request, 'team/match_detail.html', context)

@login_required
@role_required('player')
def player_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, role='player')

    try:
        player = Player.objects.get(user_profile__user=request.user)
    except Player.DoesNotExist:
        # Auto-create Player record if it doesn't exist (e.g., for admin users)
        player = Player.objects.create(
            user_profile=user_profile,
            name=request.user.username,
            shirt_number=99,
            position='MF',
            foot='right',
            playing_style='keeping'
        )

    if request.method == 'POST':
        p_form = PlayerProfileForm(request.POST, instance=player)
        u_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            return render(request, 'team/player_profile.html', {'p_form': p_form, 'u_form': u_form, 'success': True})
        else:
            return render(request, 'team/player_profile.html', {'p_form': p_form, 'u_form': u_form, 'error': True})
    else:
        p_form = PlayerProfileForm(instance=player)
        u_form = UserProfileForm(instance=user_profile)

    return render(request, 'team/player_profile.html', {'p_form': p_form, 'u_form': u_form})

@login_required
@role_required('player')
def match_schedule(request):
    try:
        player = Player.objects.get(user_profile__user=request.user)
    except Player.DoesNotExist:
        player = None

    upcoming_matches = Match.objects.filter(datetime__gte=timezone.now()).order_by('datetime')
    
    attendance_map = {}
    if player:
        attendances = Attendance.objects.filter(player=player, match__in=upcoming_matches)
        for att in attendances:
            attendance_map[att.match.id] = att.status

    # Attach status to match objects for easier template rendering
    for match in upcoming_matches:
        match.user_status = attendance_map.get(match.id, 'Not Registered')

    return render(request, 'team/match_schedule.html', {'matches': upcoming_matches})

from .forms import AttendanceForm
from .models import Attendance, Match, Player
from django.forms import modelformset_factory
from django.utils import timezone

@login_required
@role_required('player')
def register_attendance(request):
    try:
        player = Player.objects.get(user_profile__user=request.user)
    except Player.DoesNotExist:
        return HttpResponseForbidden("Player profile not found.")

    upcoming_matches = Match.objects.filter(datetime__gte=timezone.now()).order_by('datetime')

    AttendanceFormSet = modelformset_factory(Attendance, form=AttendanceForm, extra=0, can_delete=False)

    # Create initial formset data for matches without existing attendance
    attendance_qs = Attendance.objects.filter(player=player, match__in=upcoming_matches)
    attended_match_ids = [a.match.id for a in attendance_qs]
    to_create_matches = [m for m in upcoming_matches if m.id not in attended_match_ids]

    # Create Attendance objects if not existing yet for the player
    for match in to_create_matches:
        Attendance.objects.create(player=player, match=match, status='maybe')

    attendance_qs = Attendance.objects.filter(player=player, match__in=upcoming_matches)

    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST, queryset=attendance_qs)
        if formset.is_valid():
            formset.save()
            return render(request, 'team/register_attendance.html', {'formset': formset, 'success': True})
        else:
            return render(request, 'team/register_attendance.html', {'formset': formset, 'error': True})
    else:
        formset = AttendanceFormSet(queryset=attendance_qs)

    return render(request, 'team/register_attendance.html', {'formset': formset})

from django.db.models import Count, Q

@login_required
@role_required('player')
def player_stats(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, role='player')

    try:
        player = Player.objects.get(user_profile__user=request.user)
    except Player.DoesNotExist:
        # Auto-create Player record if it doesn't exist
        player = Player.objects.create(
            user_profile=user_profile,
            name=request.user.username,
            shirt_number=99,
            position='MF',
            foot='right',
            playing_style='keeping'
        )

    total_matches = player.matches_played
    total_goals = player.goals
    total_assists = player.assists

    # Calculate win rate (assumes Match model records score as 'team_score-opponent_score')
    matches = Match.objects.filter(players=player)
    wins = 0
    for match in matches:
        if match.score:
            scores = match.score.split('-')
            if len(scores) == 2:
                team_score = int(scores[0])
                opponent_score = int(scores[1])
                if team_score > opponent_score:
                    wins += 1
    win_rate = (wins / matches.count()) * 100 if matches.count() > 0 else 0

    context = {
        'player': player,
        'total_matches': total_matches,
        'total_goals': total_goals,
        'total_assists': total_assists,
        'average_rating': player.average_rating,
        'win_rate': win_rate,
    }
    return render(request, 'team/player_stats.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create default UserProfile
            UserProfile.objects.create(user=user, role='player')
            login(request, user)
            return redirect('team:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def landing(request):
    return render(request, 'team/landing.html')
