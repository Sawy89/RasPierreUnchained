import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from . import models


def xmasg_extraction(room_id):
    '''
    Run a random extraction for the Xmas gift of the selected room
    '''
    room = models.Room.objects.get(id=room_id)
    room_members = models.RoomMember.objects.filter(room=room)
    # ToDo: check and add the same member to exclusions
    
    # Cycle on room members to get J as expected
    members = {}
    for u in room_members.all():
        exc = [i[0] for i in u.exclusion.all().values_list('id')]
        members[u.member.id] = exc
    
    # Permutation = extraction
    members_receiver = xmasg_perm(members)

    # Save receiver
    for u in room_members:
        user_receiver = User.objects.get(id=members_receiver[u.id])
        u.receiver=user_receiver
        u.save()



def xmasg_extraction_test(room_id):
    ''' For testing the scheduler '''
    from_mail = 'dennytool@gmail.com'
    oggetto = "Prova n2"
    room = models.Room.objects.get(id=room_id)
    testo = f"Prova numero 2 per la stanza di numero {room_id} che si chiama {room.name}"
    # Send mail
    print('Invio la mail')
    send_mail(oggetto, testo, from_mail, ['terreno@eviso.it'])


# %% Extraction
def xmasg_perm(J):
    '''
    Function for performing the permutation
    INPUT: J is a dict containing all members as keys (django user_id) and the values are 
            user_id of exclusions!
    '''
    # ToDO: add max number of cycle, and check permutation possible
    # init
    M = list(J.keys())      # list of who_give index
    done = False                  # permutation done and correct!
    D = random.sample(M, len(M))  # 1st permutation (list of who_receive index)
    n_cycle = 0
    
    # permutation and check till result is OK
    while done == False:
        n_cycle += 1
        # print('--> permut N '+str(n_cycle))
        
        # permutation
        D = random.sample(M, len(M))  # permutation (list of who_receive index)
        done = True
        
        # check exclusion
        for i in range(len(M)):
            if D[i] in J[M[i]]:
                done = False    # permutation NO OK: redo!
    
    # prepare output
    receiver = {}
    for i in range(len(M)):
        receiver[M[i]] = D[i]
    
    # print('--> PERMUTATION OK!!!')
    return receiver