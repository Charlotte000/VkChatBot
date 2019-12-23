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
	ctx.reply("В процессе1...")
	let pyProg = spawn('python', ['eduTatarParser.py'])
	ctx.reply("В процессе2...")
	pyProg.stdout.on('data', (data) => {
		ctx.reply("В процессе3...")
		let st = data.toString('utf-8');
		let result = Buffer.from(st, 'base64').toString('utf-8');
		ctx.reply(result);
	});
	pyProg.stderr.on('data', (data) => {
		console.log(data);
		ctx.reply(data.toString());
	});
	pyProg.on('error', (err) => {
		console.log(err);
		ctx.reply(err.toString());
	});

});

bot.on((ctx) => {
	ctx.reply(ctx.message.body);
})
app.use(bodyParser.json())
 
app.post('/', bot.webhookCallback)
 
app.listen(process.env.PORT || 8000, () => console.log("Start!"))