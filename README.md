METHOD      URL                             DESCRIP                         RETURN
------------------------------------------------------------------------------
POST        /TASKS                          NEW TASK                        201
GET         /TASKS                          LIST TASKS                      200
GET         /TASKS/SITUACAO                 LIST TASKS BY SITUATION         200
GET         /TASKS/NP                       FILTER BY LEVEL AND PRIORITY    200
GET         /TASKS/{TAREFA_ID}              GET A TASK                      200
DELETE      /TASKS/{TAREFA_ID}              DELETE A TASK                   204
PUT         /TASKS/{TAREFA_ID}/INICIAR      START TASK                      200
PUT         /TASKS/{TAREFA_ID}/PENDER       OUTSTANDING TASK                200
PUT         /TASKS/{TAREFA_ID}/CANCELAR     CANCEL TASK                     200
PUT         /TASKS/{TAREFA_ID}/RESOLVER     SOLVE TASK                      200