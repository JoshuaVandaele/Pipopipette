"use-strict";
const CONFIG = require('../config.js');
const crypto = require('crypto');

//Function used to init the API routes used to manage a game
module.exports = async(app)=>{

  app.post('/start', (req, res) => {
    const userId = req.body.userId;
    const serverToken = req.body.serverToken;
    if(userId && serverToken){
      //Values correctly sent, we will check that they are valid
      if(serverToken === CONFIG.SERVER_TOKEN){
        //OK
        const token = crypto.randomBytes(16).toString('hex');
        res.json({ token });
      }else{
        //Error
        res.status(401).json({ message: "Access denied" });
      }

    }else{
      res.status(400).json({message: 'Invalid request !',
        valid_query: {userId:"int",serverToken:"string"}
      });
    }
  });

}
