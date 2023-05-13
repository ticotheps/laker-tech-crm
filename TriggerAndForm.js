function makeStandChkIn() {
  var standardCheckIn = FormApp.openByUrl('https://docs.google.com/forms/d/1KifzDMi_XmAhaS8St8O38eaOZvOPrQFoo43Wq05k14Y/edit')
  ScriptApp.newTrigger('checkIn')
    .forForm(standardCheckIn)
    .onFormSubmit()
    .create();
};

function wheresMyCharge() {
  Logger.log(getFormPrice('Charger'))
}

function getFormPrice(item) {
  let formWithPrices = 'https://docs.google.com/forms/d/1KifzDMi_XmAhaS8St8O38eaOZvOPrQFoo43Wq05k14Y/edit';

  let items = FormApp.openByUrl(formWithPrices).getItems();
  let checkItems = FormApp.openByUrl(formWithPrices).getItems().map((item) => item.getTitle());
  let priceInd = checkItems.indexOf('Faulty Items')
  let prices = items[priceInd].asCheckboxItem().getChoices();
  
  for (let i = 0; i < prices.length; i++) {
    let val = prices[i].getValue().toString();
    if (val.includes(item)) {
      return val
    }
  }
}