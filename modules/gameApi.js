"use-strict";
const CONFIG = require('../config.js');
const crypto = require('crypto');
const databaseManager = require('./database.js');
const axios = require('axios');

//Function used to init the API routes used to manage a game
module.exports = async(app)=>{

  app.post('/start', async(req, res) => {
    const userId = req.body.userId;
    const serverToken = req.body.serverToken;
    const replyPort = req.body.replyPort;
    if(userId && serverToken && replyPort){
      //Values correctly sent, we will check that they are valid
      if(serverToken === CONFIG.SERVER_TOKEN){
        //OK
        const token = crypto.randomBytes(16).toString('hex');

        let database = await databaseManager.readFile(CONFIG.DATABASE_NAME);
        if(database.pendingClient){
          //Someone else is waiting, we will start a new game
          if(req.ip == database.pendingClient.ip && replyPort == database.pendingClient.port){
            //Client already waiting
            res.status(401).json({ message: "You're already waiting" });return;
          }

          database.runningGames.push([
            database.pendingClient,
            {
              token: token,
              ip: req.connection.remoteAddress,
              port: replyPort
            }
          ]);//We can now create a new game and push clients in this game

          database.pendingClient = null;
          databaseManager.writeFile(CONFIG.DATABASE_NAME, database);

          res.json({ token, state:"READY" });

        }else{
          //We will have to wait for someone else to login
          database.pendingClient = {
            token: token,
            ip: req.ip,
            port: replyPort
          };
          databaseManager.writeFile(CONFIG.DATABASE_NAME, database);
          res.json({ token, state:"WAITING" });
        }


      }else{
        //Error
        res.status(401).json({ message: "Access denied" });
      }

    }else{
      res.status(400).json({message: 'Invalid request !',
        valid_query: {userId:"int",serverToken:"string", replyPort:"int"}
      });
    }
  });


  app.post('/next', async(req, res) => {
    const token = req.body.token;
    if(token){

      let database = await databaseManager.readFile(CONFIG.DATABASE_NAME);

      let foundGameId;//Will store the index of game where client is
      let fondUserId;//Will store the index of the user in this game
      for(let i=0; i<database.runningGames.length; i++){//For each game
        for(let j=0; j<database.runningGames[i].length; j++){//For each client in it
          if(database.runningGames[i][j].token == token){//If the saved client has the same token as the token given in request
            foundGameId = i;
            fondUserId = j;
            break;
          }
        }
        if(foundGameId)break;
      }

      if(foundGameId!==undefined){
        //Token found
        let data = req.body;
        delete data.token;

        for(let i=0; i<database.runningGames[foundGameId].length; i++){
          if(i == fondUserId)continue;
          axios.post("http://"+database.runningGames[foundGameId][i].ip+":"+database.runningGames[foundGameId][i].port+"/next", data);
        }


        res.json({ message:"OK" });
      }else{
        //The token wasn't found...
        res.status(401).json({ message: "Access denied" });
      }

    }else{
      res.status(400).json({message: 'Invalid request !',
        valid_query: {token:"token",anythingYouWantToSend:"Any"}
      });
    }
  });

  app.post('/end', async(req, res) => {
    const token = req.body.token;
    if(token){

      let database = await databaseManager.readFile(CONFIG.DATABASE_NAME);

      let foundGameId;//Will store the index of game where client is
      for(let i=0; i<database.runningGames.length; i++){//For each game
        for(let j=0; j<database.runningGames[i].length; j++){//For each client in it
          if(database.runningGames[i][j].token == token){//If the saved client has the same token as the token given in request
            foundGameId = i;
            break;
          }
        }
        if(foundGameId)break;
      }

      if(foundGameId!==undefined){
        //Token found

        database.runningGames.splice(foundGameId, 1);//Remove game from database
        await databaseManager.writeFile(CONFIG.DATABASE_NAME, database);

        res.json({ message:"OK" });
      }else{
        //The token wasn't found...
        res.status(401).json({ message: "Access denied" });
      }

    }else{
      res.status(400).json({message: 'Invalid request !',
        valid_query: {token:"token"}
      });
    }
  });

}
