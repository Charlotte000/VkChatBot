const TOKEN = process.env.token;
const CONFIRMATION = process.env.confirmation


const express = require('express')
const bodyParser = require('body-parser')
const VkBot = require('node-vk-bot-api')
 
const app = express()

const spawn = require('child_process').spawn

const bot = new VkBot({
  token: TOKEN,
  confirmation: CONFIRMATION,
})
 
bot.command('/дз', (ctx) => {
	ctx.reply("В процессе...")
	let pyProg = spawn('python', ['eduTatarParser.py'])
	pyProg.stdout.on('data', (data) => {
		let st = data.toString('utf-8');
		let result = Buffer.from(st, 'base64').toString('utf-8');
		ctx.reply(result);
	});

});

bot.on((ctx) => {
	ctx.reply(ctx.message.body);
})
app.use(bodyParser.json())
 
app.post('/', bot.webhookCallback)
 
app.listen(80, () => console.log("Start!"))