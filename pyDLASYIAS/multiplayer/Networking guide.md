A message about networking in pyDLASYIAS:
-----------------------------------------

About received data on the server and what it does...

    Let's look at this example

        b'goto cam1b'

     The server should "transform" the data into a string and then split the
     string into a list. Finally it should check the words in the list.

     Valid words:

    -Animatronics:

        +Bear, Rabbit and Chicken (AKA Freddy, Bonnie and Chica):

            First Words:
                'goto', '', '', '', ''.

            Second Words:
                *all of the cameras*, 'leftdoor', 'rightdoor', 'inside'

        +Fox (AKA Foxy):

            First Words:
                'status', '', ''

            Second Words:
                'up', 'down', *numbers*

        +Guard:

            First Words:
                'scene', 'check', 'leftdoor', 'rightdoor', 'leftlight',
                'rightlight'

            Second Words:
                'office', 'cam', 'true', 'false', *all of the cameras*
