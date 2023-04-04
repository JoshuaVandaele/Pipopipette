# Game server

This node server is used to connect two clients together, and allows to play multiplayer.

## How to use ?

There are three **POST** API routes :

### /start :

Example request :
```json
{
	"userId":40, //ID of the user currently playing. 
	"serverToken":"serverToken", //Security token
	"replyPort": 43 //Where should the server send information about current game
}
```

Example answer :
```json
{
  "token": "c845324cc47bcaac98de2892afc742ee", //Identification token
  state:"WAITING"
}
```

About state, it will be `WAITING` if you must wait someone else to play. If you receive `READY`, you already have someone else to play with, and can start immediately to play.
Users who receive `WAITING` are always the second to play.

### /next :

Example request :

```json
{
"token":"c845324cc47bcaac98de2892afc742ee",
"anythingYouWantToSend":"Yes",
. . .
}
```

You need to give the token, but are free to add anything you want.
Everything, except the token will be sent to others clients playing with you.

Example answer :
```json
{
	"message": "OK"
}
```

#### Receiving /next events

When someone is using /next, you will have to manage receiving server request.
You should create a small HTTP server, listening for POST requests. Create the server on the
`replyPort` you defined earlier

### /end :

Example request :
```json
{
"token":"c845324cc47bcaac98de2892afc742ee"
}
```

Example answer :
```json
{
    "message": "OK"
}
```

Using this will stop the current game. Tokens will be deleted, and clients will have to use
**/start** again to start a new game.
