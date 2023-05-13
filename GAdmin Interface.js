// jshint esversion: 9
// jshint laxbreak: true


const GAM = new (function () {
  let _accessToken = null;

  const encodeQueryString = obj => {
    const pairs = [];
    for (const key of Object.keys(obj)) {
      const value = obj[key];
      if (typeof value === 'undefined') {
        continue;
      }
      if ((typeof value === 'object') && (value.constructor === Array)) {
        for (const el of value) {
          pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(el.toString()));
        }
      }
      else { pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(value.toString())); }
    }
    return pairs.join('&');
  };

  const _getAccessToken = () => {
    if (!_accessToken) {
      _accessToken = ScriptApp.getOAuthToken();
    }
    return _accessToken;
  };

  const _apiPutter = ({path, params, payload}) => {
    let url = `https://admin.googleapis.com/admin/directory/v1/${path}`;
    if (params) {
      const q = encodeQueryString(params);
      if (q.length) {
        url += '?' + q;
      }
    }
    let request = {
      method: 'GET',
      muteHttpExceptions: true,
      headers: {
        'authorization': `Bearer ${_getAccessToken()}`
      }
    };
    if (payload) {
      request = {
        ...request,
        method: 'PUT',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    }
    // Logger.log(url);
    // Logger.log(request);
    response = UrlFetchApp.fetch(url, request);

    if (response.getResponseCode() !== 200) {
      throw new Error(response.getContentText());
    }
    return JSON.parse(response.getContentText());
    
  };

  const _apiPostman = ({path, params, payload}) => {
    let readable = {}
    let url = `https://admin.googleapis.com/admin/directory/v1/${path}`;
    if (params) {
      const q = encodeQueryString(params);
      if (q.length) {
        url += '?' + q;
      }
    }
    let request = {
      method: 'GET',
      muteHttpExceptions: true,
      headers: {
        'authorization': `Bearer ${_getAccessToken()}`,
        'Content-Type': 'application/json'
      }
    };
    if (payload) {
      request = {
        ...request,
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    }
    // Logger.log(url);
    // Logger.log(request);
    response = UrlFetchApp.fetch(url, request)
      reponse => reponse.text()
      text => {
        try {
          const data = JSON.parse(text);
          readable = data
        } catch(err) {
          readable = text
        }
      }
    return readable;
    
  };

  const _paginatedApiCall = ({path, params, payload, ...opts}) => {
    if (!payload) {
      params = params || {};
    }

    let pageToken = "";
    let results = [];

    do {

      if (pageToken) {
        params = {...params, pageToken: pageToken};
      }

      const body = _apiPutter({path, params, payload, ...opts});

      if (Object.keys(body).length === 0) {
        break;
      }

      results.push(body);
      pageToken = body.nextPageToken;

      if (!pageToken) {
        break;
      }

    } while (pageToken);

    return results;
  };

  this.getUserList = (q, fieldSet) => {

    let userList = [];

    let uPages = _paginatedApiCall({
      path: `users`,
      params: {
        customer: `my_customer`,
        projection: 'full',
        query: `${q}`
      }
    });

    // Logger.log(uPages[0].users[1]);

    for (let userPgNum = 0; userPgNum < uPages.length; userPgNum++) {
      for (let userNum = 0; userNum < uPages[userPgNum].users.length; userNum++) {
        let CurrentUser = uPages[userPgNum].users[userNum]
        let userLineItem = [];
        userLineItem.push(CurrentUser.primaryEmail)
        if (fieldSet && fieldSet.length !== 0) {
          for (let fieldNum = 1; fieldNum < fieldSet.length; fieldNum++) {
            let currentField = fieldSet[fieldNum]
            userLineItem.push(getObjectProperty(CurrentUser, currentField))
          }
        }
        userList.push(userLineItem);
      }
    }

    return userList;

  };

  this.getUser = (userKey) => {
    if (!userKey) {
      throw new Error('Please input resource object.');
    }

    if (typeof userKey !== 'string') {
      userKey = userKey.toString()
    }

    if (!userKey.endsWith('@lakerschools.org')) {
      // Logger.log(`${userKey} is not a Lakers email!`)
      return
    }

    let gottenUser = _apiPutter({
      path: `users/${userKey}`,
      params: {
        projection: 'full'
      }
    });

    // Logger.log(gottenUser);
    return gottenUser;
  };

  this.getUserName = (userKey) => {
    // Logger.log(userKey);
    if (!userKey) {
      throw new Error('Please input resource object.');
    }

    if (typeof userKey !== 'string') {
      userKey = userKey.toString()
    }

    if (!userKey.endsWith('@lakerschools.org')) {
      // Logger.log(`${userKey} is not a Lakers email!`)
      return `${userKey} is not a Lakers email!`
    }

    let gottenUser = _apiPutter({
      path: `users/${userKey}`,
      params: {
        projection: 'full',
        fields: 'name',
        viewType: 'domain_public'
      }
    });

    return gottenUser.name.fullName;
  };

  this.multiUpdateUser = (fieldsList, valuesArray) => {

    let allTops = getHighestLevelProperties(fieldsList);
    allTops.shift()

    let urlFields = allTops.toString();
    // Logger.log(urlFields);

    for (let row = 0; row < valuesArray.length; row++) {
        let userKey = valuesArray[row][0];
        let fullPayload = createObjectFromPropertyStrings(fieldsList, valuesArray[row], 'customSchemas.Enhanced_desktop_security.AD_accounts.0', 'type', 'work')
        // Logger.log(fullPayload)
        try {
          let gottenUser = _apiPutter({
            path: `users/${userKey}?fields=primaryEmail,${urlFields}`,
            payload: fullPayload
          });
          // Logger.log(gottenUser);
        } catch {
          // Logger.log('could not edit user')
        }
    }
  };

  this.getDevice = (deviceId) => {
    let gottenDevice = _apiPutter({
      path: `customer/my_customer/devices/chromeos/${deviceId}`,
      params: {
        projection: 'full'
      }
    });

    // Logger.log(gottenDevice);
    return gottenDevice;
  };
  
  this.getDevices = (q, fieldSet) => {
    let deviceList = [];
      if (q.includes('orgUnitPath:')) {
      let splitQ = q.split('orgUnitPath:');

      let orgEndIndex = splitQ[1].lastIndexOf(' ', splitQ[1].indexOf(':')); // find the last space before the next colon
      var org = splitQ[1].substring(0, orgEndIndex).trim();
      var rest = splitQ[0].trim() + ' ' + splitQ[1].substring(orgEndIndex + 1).trim();
    } else {
        var org = "/"
        var rest = q
    };
  
    let dPages = _paginatedApiCall({
      path: 'customer/my_customer/devices/chromeos',
      params: {
        includeChildOrgunits: true,
        maxResults: 500,
        orderBy: "LAST_SYNC",
        sortOrder: "DESCENDING",
        orgUnitPath: org,
        projection: "full",
        query: rest
      }
    });

    // Logger.log(dPages[0].chromeosdevices[0]);


    // List of valid 'CurentUser.' endings can be found at https://developers.google.com/admin-sdk/directory/reference/rest/v1/users#UserName
    for (let devicePgNum = 0; devicePgNum < dPages.length; devicePgNum++) {
      for (let deviceNum = 0; deviceNum < dPages[devicePgNum].chromeosdevices.length; deviceNum++) {
        let CurrentDevice = dPages[devicePgNum].chromeosdevices[deviceNum]
        let deviceLineItem = [];
        deviceLineItem.push(CurrentDevice.deviceId)
        deviceLineItem.push(CurrentDevice.etag.replaceAll('\"', ''))
        if (fieldSet && fieldSet.length !== 0) {
          for (let fieldNum = 2; fieldNum < fieldSet.length; fieldNum++) {
            let currentField = fieldSet[fieldNum]
            deviceLineItem.push(getObjectProperty(CurrentDevice, currentField))
          }
        }
        deviceLineItem[2] = false; // Defaults Updating field to false
        deviceList.push(deviceLineItem);
      }
    }

    return deviceList;

  };

  this.updateDevice = (deviceId, deviceObj) => {
    let annotateDevice = _apiPutter({
      path: `customer/my_customer/devices/chromeos/${deviceId}`,
      payload: deviceObj
    });
    Logger.log(annotateDevice);
  }

  this.wipeDevice = (deviceId) => {
    let wipeCommand = {
      "commandType": "WIPE_USERS"
    }
    let wipeDevice = _apiPostman({
      path: `customer/my_customer/devices/chromeos/${deviceId}:issueCommand`,
      payload: wipeCommand
    })
    Logger.log(wipeDevice);
  }

  this.changeDeviceStatus = (deviceId, action) => {
    let deviceAction = {
      "action": `${action}`
    }
    let changeDevStatus = _apiPostman({
      path: `customer/my_customer/devices/chromeos/${deviceId}/action`,
      payload: deviceAction
    })
    Logger.log(changeDevStatus)
  }

  this.rebootDevice = (deviceId) => {
    let rebootCommand = {
      "commandType": "REBOOT"
    }
    let rebootDevice = _apiPostman({
      path: `customer/my_customer/devices/chromeos/${deviceId}:issueCommand`,
      payload: rebootCommand
    })
    Logger.log(rebootDevice);
  }

  this.multiUpdateDevice = (fieldsList, valuesArray) => {

    let allTops = getHighestLevelProperties(fieldsList);
    allTops.shift();

    for (let field = 0; field < allTops.length; field++) {
      if (!devUpdFields.includes(allTops[field])) {
        allTops[field] = ''; 
      }
    }

    let urlFields = allTops.toString();
    Logger.log(urlFields);

    for (let row = 0; row < valuesArray.length; row++) {
      if (!valuesArray[row][1] === true) {
        Logger.log(valuesArray[row][1])
        return
        } else {
        let deviceId = valuesArray[row][0];
        let sheetToCB = createObjectFromPropertyStrings(fieldsList, valuesArray[row], '', '', '', devUpdFields)
        Logger.log(sheetToCB);
        GAM.updateDevice(deviceId, sheetToCB);

        if (fieldsList.includes('Wipe?') && valuesArray[row].includes('WIPE_USERS')) {
          GAM.wipeDevice(deviceId);
        }

        if (fieldsList.includes('status')) {
          let statusIndex = fieldsList.indexOf('status')
          let statusCell = valuesArray[row][statusIndex]
          switch (statusCell) {
            case 'ACTIVE': 
              action = 'reenable';
              break;
            case 'DISABLED': 
              action = 'disable';
              break;
            default: {
              action = null;
              Logger.log(`Could not set ${statusCell} to a device`)
            }
          }
          GAM.changeDeviceStatus(deviceId, action)
        }
      }
    }
  };

  this.testing = () => {
    let statusCell = 'DISABLED';
    Logger.log(statusCell);
    switch (statusCell) {
      case 'ACTIVE': 
        action = 'reenable';
        break;
      case 'DISABLED': 
        action = 'disable';
        break;
      default: {
        action = null;
        Logger.log(`Could not set ${statusCell} to a device`)
      }
    }
    let deviceAction = {
      "action": action
    }
    Logger.log(deviceAction)
  };
  

})();

function testing () {
  let checkOneTwo = GAM.getDevice('21320244-0ba3-4a8f-aa65-3cf06e5b71e0')
  let lastTime = checkOneTwo.activeTimeRanges[checkOneTwo.activeTimeRanges.length-1].date + " " + new Date(checkOneTwo.activeTimeRanges[checkOneTwo.activeTimeRanges.length-1].activeTime).toTimeString();
  Logger.log(checkOneTwo.activeTimeRanges);
  Logger.log(lastTime);
}

function getLastTime(Device) {
  let lastTime = Device.activeTimeRanges[Device.activeTimeRanges.length-1].date + " at " + new Date(Device.activeTimeRanges[Device.activeTimeRanges.length-1].activeTime).toTimeString();
  return lastTime
}

const devUpdFields = ['annotatedUser', 'annotatedAssetId', 'notes', 'status', 'orgUnitPath', 'annotatedLocation'];

const getObjectProperty = (obj, propertyString) => {
  const properties = propertyString.split(".");
  let result = obj;
  for (let i = 0; i < properties.length; i++) {
    const prop = properties[i];
    if (result === undefined) {
      break;
    }
    if (Array.isArray(result)) {
      const arrayIndex = parseInt(prop, 10);
      if (arrayIndex < 0) {
        result = result[result.length - (arrayIndex * -1)]
      } else {
      result = result[arrayIndex];
      }
      if (result && typeof result === "object" && properties[i + 1]) {
        result = getObjectProperty(result, properties.slice(i + 1).join("."));
        break;
      }
    } else {
      result = result[prop];
      if (typeof result === "object" && result !== null && properties[i + 1]) {
        result = getObjectProperty(result, properties.slice(i + 1).join("."));
        break;
      }
    }
  }
  return result;
};

const createObjectFromPropertyStrings = (propertyStrings, values, propertyToModify, keyToAdd, valueToAdd, filterArray) => {
  const result = {};
  propertyStrings.forEach((propertyString, index) => {
    const keys = propertyString.split(".");
    let obj = result;
    keys.forEach((key, i) => {
      if (!obj[key]) {
        obj[key] = isNaN(parseInt(keys[i+1])) ? {} : [];
      }
      if (i === keys.length - 1) {
        if (Array.isArray(obj[key])) {
          obj[key].push(values[index]);
        } else {
          obj[key] = values[index];
        }
      }
      obj = obj[key];
    });
  });
  // Inject a new key-value pair into the specified property
  if (propertyToModify && keyToAdd && valueToAdd) {
    const keys = propertyToModify.split(".");
    let obj = result;
    keys.forEach((key, i) => {
      if (!obj[key]) {
        obj[key] = {};
      }
      if (i === keys.length - 2) {
        obj[key][keys[keys.length - 1]] = {
          ...obj[key][keys[keys.length - 1]],
          [keyToAdd]: valueToAdd
        };
      }
      obj = obj[key];
    });
  }

  if (!filterArray)
  return result;
  else {
    const filteredByKey = Object.fromEntries(
      Object.entries(result).filter(([key, value]) => filterArray.includes(key))
    )
    return filteredByKey;
  }
};

const getHighestLevelProperties = (propertyStrings) => {
  const properties = new Set();
  propertyStrings.forEach((propertyString) => {
    const firstProp = propertyString.split(".")[0];
    if (firstProp) {
      properties.add(firstProp);
    }
  });
  return [...properties];
};

Array.prototype.last = function() {
    return this[this.length - 1];
}