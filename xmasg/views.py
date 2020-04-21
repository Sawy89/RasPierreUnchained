from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from string import Template
from django.utils import timezone
import math
from . import forms, models
import json


# %% Support Functions
def prepare_sidebar(current_user):
    '''
    Function for getting info for sidebar
    '''
    sidebar_data = {}
    
    sidebar_data['rooms'] = models.Room.objects.filter(end_date__gte=timezone.now()).exclude(member=current_user).all()   # Get available rooms
    sidebar_data['myrooms'] = models.Room.objects.filter(member=current_user).all()   # ToDO: add filter on user subscribed

    return sidebar_data

def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


# %% Pages
@login_required
def index(request):
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)

    return render(request, 'xmasg/index.html', {"sidebar_data": sidebar_data}) 


@login_required
def room(request, pk):
    # Get room
    try:
        room = models.Room.objects.get(id=pk)
        room_members = models.RoomMember.objects.filter(room=room).all()
        user_member = models.RoomMember.objects.filter(room=room).filter(member=request.user).first()
        
        # aggiungere info admin e esclusioni!!
        room.user_member = user_member
        room.end_date_str = timezone.localtime(room.end_date).strftime('%d-%m-%Y %H:%M') # pay attention to tzinfo
        room.gift_date_str = timezone.localtime(room.gift_date).strftime('%d-%m-%Y %H:%M') # pay attention to tzinfo
        # delta = room.end_date - timezone.now()
        # room.end_date_delta_str = strfdelta(delta, "%D giorni, %H ore %M minuti e %S secondi!")
        for u in room_members:
            u.is_your_exclusion = user_member.has_as_exclusion(u.member) if user_member != None else False
            if u.member == request.user and u.is_admin:
                room.is_user_admin = True
    except models.Room.DoesNotExist:
        raise Http404('Room does not exist')
    
    # Get form
    room_members_list = [u.member for u in room_members]
    if not(request.user in room_members_list):
        form = forms.RoomMemberForm()
        form.fields['user_id'].initial = request.user.id
        form.fields['room_id'].initial = room.id
    else:
        form = None
    
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)
    
    return render(request, 'xmasg/room.html', {"sidebar_data": sidebar_data, 
                                                "room": room, "room_members": room_members,
                                                "form_add_member": form}) 

@login_required
def room_add_member(request):
    '''
    Add a member to a room
    '''
    # Read form
    if request.method == 'POST':
        form = forms.RoomMemberForm(request.POST)
        if form.is_valid():
            room = models.Room.objects.get(id=form.cleaned_data['room_id'])
            user = User.objects.get(id=form.cleaned_data['user_id'])
            room_members = models.RoomMember.objects.filter(room=room).all()
            if room.extraction_done != '':
                return HttpResponseBadRequest('Extraction already done')
            if user not in [u.member for u in room_members]:
                room_member = models.RoomMember.objects.create(room=room, member=user, is_admin=False)
                room_member.exclusion.add(request.user)
                room_member.save()
            return redirect('xmasg_room', pk=room.id)
        return HttpResponseBadRequest('Wrong add member request')
    return HttpResponseBadRequest('Wrong type request')


@login_required
def room_new(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            obj = form.save()
            room_member = models.RoomMember.objects.create(room=obj, member=request.user, is_admin=True)
            room_member.exclusion.add(request.user)
            room_member.save()
            return redirect('xmasg_index')
    else:
        form = forms.RoomForm()
    # Get data for sidebar
    sidebar_data = prepare_sidebar(request.user)
    return render(request, 'xmasg/room_new.html', {"sidebar_data": sidebar_data,
                                                    "form": form}) 


# %% API for AJAX
# @login_required
class RoomMemberModification(View):
    
    @method_decorator(login_required)
    def post(self, request):
        '''
        Modify the exclusion or admin
        '''
        try:
            data = json.loads(request.body) #{'roomId': room_id, 'elName': elName, 'elMemberId': elMemberId, 'elChecked': elChecked}
            print(data)
            room = models.Room.objects.get(id=data['roomId'])
            member = User.objects.get(id=data['elMemberId'])

            # Extraction already done
            if room.extraction_done != '':
                return HttpResponseBadRequest('Extraction already done')

            if data['elName'] == 'is-your-exclusion':
                # is-your-exclusion
                room_member = models.RoomMember.objects.filter(room=room).filter(member=request.user).first()
                if data['elChecked'] == True:
                    room_member.exclusion.add(member)
                    room_member.save()
                else:
                    if member == request.user:
                        return JsonResponse({'message': 'Can not remove exclusion from yourself!'}, status=400)
                    else:
                        room_member.exclusion.remove(member)
                        room_member.save()
            elif data['elName'] == 'is-admin':
                # is-admin
                # ToDO aggiungere controllo: solo request.user == is_admin può modificare queste cose
                room_member = models.RoomMember.objects.filter(room=room).filter(member=member).first()
                if data['elChecked'] == True:
                    room_member.is_admin = True
                    room_member.save()
                else:
                    n_admin = 0
                    for u in models.RoomMember.objects.filter(room=room).all():
                        if u.is_admin == True:
                            n_admin += 1    # count number of admin
                    if n_admin > 1:
                        room_member.is_admin = False
                        room_member.save()
                    else:
                        return HttpResponseBadRequest('Can not remove last admin')
            else:
                return HttpResponseBadRequest('Wrong elName')

            return JsonResponse({'message': 'OK'}, status=200)
        except:
            return HttpResponseBadRequest('Something went wrong')


class RoomDateModification(View):

    def get(self, request):
        return HttpResponseBadRequest('ciao ciao')
    
    @method_decorator(login_required)
    def post(self, request):
        '''
        Modify the dates: gift date and end date
        '''
        try:
            data = json.loads(request.body) #{'roomId': room_id, 'elName': elName, 'elMemberId': elMemberId, 'elChecked': elChecked}
            print(data)
            room = models.Room.objects.get(id=data['roomId'])
            member = User.objects.get(id=request.user.id)

            if models.RoomMember.objects.filter(room=room).filter(member=member).first().is_admin == False:
                return HttpResponseBadRequest('User is not admin')

            if data['elName'] == 'enddate':
                # Extraction already done
                if room.extraction_done != '':
                    return HttpResponseBadRequest('Extraction already done')
                # End date after extraction
                if get_aware_datetime(data['elDate']) > room.gift_date:
                    return HttpResponseBadRequest("Gift date can't be before end date")
                # Save new end date
                room.end_date = get_aware_datetime(data['elDate'])
                room.save()
                return JsonResponse({'message': 'OK'}, status=200)
            elif data['elName'] == 'giftdate':
                # Gift date before extraction
                if get_aware_datetime(data['elDate']) < room.end_date:
                    return HttpResponseBadRequest("Gift date can't be before end date")
                # Save new gift date
                room.gift_date = get_aware_datetime(data['elDate'])
                room.save()
                return JsonResponse({'message': 'OK'}, status=200)
            else:
                return HttpResponseBadRequest('Wrong elName')
        except:
            return HttpResponseBadRequest('Something went wrong (code crash)')
