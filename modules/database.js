const fs = require('fs');

const dataFolder = "./databases/";

const defaultDatabase = {
  pendingClient: null,//Pending client, which is waiting for someone else to login
  runningGames: []//Array that contains array of clients connected together in game
}

/* Module used to store data in a file */

module.exports = {
  readFile: async function(filePath){
    try{
      const data = await fs.promises.readFile(dataFolder + filePath, 'utf-8');
      return JSON.parse(data);
    }catch(err){
      throw `Error while reading saved file : ${err}`;
    }
  },

  writeFile: async function(filePath, data){
    const fullPath = dataFolder + filePath;
    try {
      await fs.promises.writeFile(fullPath, JSON.stringify(data));
    } catch (err) {
      throw `Error while writing to file: ${err}`;
    }
  },

  appendToFile: async function(filePath, data){
    try{
      await fs.promises.appendFile(dataFolder + filePath, JSON.stringify(data));
    }catch(err){
      throw `Error while appending to a saved file : ${err}`;
    }
  },

  clearFile: async function(filePath){
    try{
      await fs.promises.writeFile(dataFolder + filePath, '');
    }catch(err){
      throw `Error while deleting from a saved file : ${err}`;
    }
  },

  createFileWithDefaults: async function(filePath){
    const fullPath = dataFolder + filePath;
    if (fs.existsSync(fullPath))return;//This file already exists, so we don't need to create it
    try{
      await fs.promises.writeFile(fullPath, JSON.stringify(defaultDatabase));
    }catch(err){
      throw `Error while creating file with defaults : ${err}`;
    }
  }
};
