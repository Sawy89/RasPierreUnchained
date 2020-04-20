import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from . import models


def xmasg_extraction(room_id):
    '''
    Run a random extraction for the Xmas gift of the selected room
    '''
    room = models.Room.objects.get(id=room_id)
    try:
        room_members = models.RoomMember.objects.filter(room=room)
        
        # Cycle on room members to get J as expected
        members = {}
        for u in room_members.all():
            exc = [i[0] for i in u.exclusion.all().values_list('id')]
            if u.member.id not in exc:
                exc.append(u.member.id)
            members[u.member.id] = exc
        
        # Permutation = extraction
        members_receiver = xmasg_perm(members)

        # Save receiver
        if members_receiver == None:
            # Save error
            room.extraction_done = f"Failure: extraction not done at {timezone.now()}"
            room.save()
        else:
            for u in room_members:
                user_receiver = User.objects.get(id=members_receiver[u.id])
                u.receiver=user_receiver
                u.save()
            # Save extraction done
            room.extraction_done = f"Success at {timezone.now()}"
            room.save()

            # ToDO: send mail to members
            for u in room_members:
                xmasg_extraction_mail(room, u)

    except:
        room.extraction_done = f"Failure for a problem (try except) at {timezone.now()}"
        room.save()



def xmasg_extraction_mail(room, member):
    '''
    Send mail with the extracted
    '''
    from_mail = 'dennytool@gmail.com'
    oggetto = f"XmasG: estrazione per {room.name}"
    testo = f"Buongiorno {member.member.first_name},\nÉ stata effettuata l'estrazione per la stanza {room.name}.\n\n"+\
        "Sei stato molto fortunato, e dovrai fare il regalo a {member.receiver.username} - {member.receiver.first_name} {member.receiver.last_name}"
    # Send mail
    print(f'Invio la mail a {member.member.mail}')
    send_mail(oggetto, testo, from_mail, [member.member.mail])


# %% Extraction
def xmasg_perm(J):
    '''
    Function for performing the permutation
    INPUT: J is a dict containing all members as keys (django user_id) and the values are 
            user_id of exclusions!
    '''
    # ToDO: check permutation possible
    # init
    M = list(J.keys())      # list of who_give index
    done = False                  # permutation done and correct!
    D = random.sample(M, len(M))  # 1st permutation (list of who_receive index)
    n_cycle = 0
    max_n_cycle = 10000
    
    # permutation and check till result is OK
    while done == False and n_cycle < max_n_cycle:
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
    if done == True:
        receiver = {}
        for i in range(len(M)):
            receiver[M[i]] = D[i]
    else:
        receiver = None
    
    # print('--> PERMUTATION OK!!!')
    return receiver