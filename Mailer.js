const me = Session.getActiveUser().getEmail();
const maskName = 'Laker Chromie Manager :)'
const maskAcc = 'lakers-device-manager@lakerschools.org';
const redirect = 'help@lakerschools.org';
const aliases = GmailApp.getAliases();





function sameUser(retUsr, retDev) {
  var msgSubj = 'Chromebook Return Reciept';

  if (!aliases.includes(maskAcc)) {
    GmailApp.sendEmail(me, 'Alias not found', 'You should check the script and the account\'s settings to make sure you spelled the alias address correctly.');
  } else {
    let maskIndex = aliases.indexOf(maskAcc);
    let msgBody = `Thank you for returning your device, ${retDev}!\nYou currently have`
    GmailApp.sendEmail(retUsr, msgSubj, msgBody, {
      'from': aliases[maskIndex],
      'name': maskName,
      'replyTo': redirect
      });
  }
};

function diffUsers(retUsr, retDev, annotUsr) {
  var msgSubj = 'Chromebook Return Reciept';
  var currOut = ACC.report(retUsr)
  if (!annotUsr) {
    devOwner = 'Unfortunately, we were unable to make sure that device was assigned to you, and so any devices below are still under your name.'
  } else {
    devOwner = `Unfortunately, that device was assigned to ` + GAM.getUserName(annotUsr) + '. Below are any devices still under your name.';
  }

  var aliases = GmailApp.getAliases();
  Logger.log(currOut)
  if (!aliases.includes(maskAcc)) {
    GmailApp.sendEmail(me, 'Alias not found', 'You should check the script and the account\'s settings to make sure you spelled the alias address correctly.');
  } else {
    let maskIndex = aliases.indexOf(maskAcc);
    let msgBody = `Thank you for returning ${retDev}!\n${devOwner}\n\nCurrently, you have checked out: \n\n${currOut}\n\nIf you still have items checked out, please see about returning those items before their due date(s), otherwise you may be charged.`
    GmailApp.sendEmail(retUsr, msgSubj, msgBody, {
      'from': aliases[maskIndex],
      'name': maskName,
      'replyTo': redirect
      });
  }

  let lakerTagRegex = /Lakers (\d){3}/gi;
  let retUsersLost = currOut.match(lakerTagRegex)
  Logger.log(retUsersLost)
  if (retUsersLost) {
    retUsersLost.forEach((lostDevTag) => LGN.missing(lostDevTag, retUsr)) 
  }
};

function thxCharger(userMail) {
  var msgSubj = 'Chromebook Charger Return Reciept';
  var currOut = ACC.report(userMail);

  var aliases = GmailApp.getAliases();
  Logger.log(currOut)
  if (!aliases.includes(maskAcc)) {
    GmailApp.sendEmail(me, 'Alias not found', 'You should check the script and the account\'s settings to make sure you spelled the alias address correctly.');
  } else {
    let maskIndex = aliases.indexOf(maskAcc);
    let msgBody = `Thank you for returning your charger!\nJust as an FYI, here is what you still have on your account.\n\nCurrently, you have checked out: \n\n${currOut}\n\nIf you still have items checked out, please see about returning those items before their due date(s), otherwise you may be charged.`
    GmailApp.sendEmail(userMail, msgSubj, msgBody, {
      'from': aliases[maskIndex],
      'name': maskName,
      'replyTo': redirect
      });
  }
}

function dueSoonMessage(userMail) {
  var msgSubj = 'Device Due-Soon Warning';
  var currOut = ACC.report(userMail);

  var aliases = GmailApp.getAliases();
  Logger.log(currOut)
  if (!aliases.includes(maskAcc)) {
    GmailApp.sendEmail(me, 'Alias not found', 'You should check the script and the account\'s settings to make sure you spelled the alias address correctly.');
  } else {
    let maskIndex = aliases.indexOf(maskAcc);
    let msgBody = `This is just a friendly heads-up that you have devices checked out that are due soon.\n\nCurrently, you have checked out: \n\n${currOut}\n\nPlease be sure to return those items before 4 PM on their due date(s), otherwise you may be charged (if you have not been already).`
    GmailApp.sendEmail(userMail, msgSubj, msgBody, {
      'from': aliases[maskIndex],
      'name': maskName,
      'replyTo': redirect
      });
  }
}

function faultyChargeMessage(userMail, items, itemsCharge) {
  var msgSubj = 'Faulty Device Reciept';
  let itemWords = textMultiples(items)

  if (!aliases.includes(maskAcc)) {
    GmailApp.sendEmail(me, 'Alias not found', 'You should check the script and the account\'s settings to make sure you spelled the alias address correctly.');
  } else {
    let maskIndex = aliases.indexOf(maskAcc);
    let msgBody = `Thank you for returning that device!\nUnfortunately, we have had to charge your account \$${itemsCharge}.00 due to the faulty ${itemWords} on return.\n\nIf you have any questions, feel free to respond to this email and we can help sort things out!`
    GmailApp.sendEmail(userMail, msgSubj, msgBody, {
      'from': aliases[maskIndex],
      'name': maskName,
      'replyTo': redirect
      });
  }
};

function missingChargeMessage(userMail, items, charge) {
  var msgSubj = 'Missing Device Charge Reciept';
  let itemWords = textMultiples(items)

  if (!aliases.includes(maskAcc)) {
    GmailApp.sendEmail(me, 'Alias not found', 'You should check the script and the account\'s settings to make sure you spelled the alias address correctly.');
  } else {
    let maskIndex = aliases.indexOf(maskAcc);
    let msgBody = `Hello!\nWe regret to inform you that because you have not turned in your ${itemWords} by their due date (today), your account has been charged \$${charge}\n\nIf you have any questions, feel free to respond to this email—please let us know if there is anything we can do to help sort this out!`
    GmailApp.sendEmail(userMail, msgSubj, msgBody, {
      'from': aliases[maskIndex],
      'name': 'Laker Chrombook Manager',
      'replyTo': redirect
      });
  }
};


function textMultiples(list) {
  let listArray = list.split(',')
  listArray.forEach((item) => Logger.log(item))
  Logger.log(listArray.length);
  switch (listArray.length) {
    case 0:
      return
    case 1:
      return listArray[0].toString()
    case 2:
      let pair = listArray[0].toString().trim() + " and " + listArray[1].trim()
      return pair
    default:
      let last = listArray.pop().toString()
      let listedString = listArray.join(",") + ", and " + last.trim()
      return listedString
  }
}

function mailTestr() {
  Logger.log(GmailApp.getAliases())
}