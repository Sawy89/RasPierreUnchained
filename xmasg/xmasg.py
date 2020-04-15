import random
from django.core.mail import send_mail
from . import models


def stampa(testo):
    from_mail = 'dennytool@gmail.com'
    oggetto = "Prova n2"
    testo = f"Prova numero 2 per la stanza {testo}"
    # Send mail
    print('Invio la mail')
    send_mail(oggetto, testo, from_mail, ['terreno@eviso.it'])




# %% Extraction
def xmasg_perm(J):
    '''
    Function for performing the permutation
    INPUT: J is a list of all the exclusions (every exclusion is a list)
            every people is mapped with a number, and it should exclude at least himself
    '''
    # init
    n = len(J)
    M = list(range(n))             # list of who_give index
    done = False                 # permutation done and correct!
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
            if D[i] in J[i]:
                done = False    # permutation NO OK: redo!
    
    # print('--> PERMUTATION OK!!!')
    return D