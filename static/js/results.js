const LOG_REFRESH = 3000; // ms
const LOG_REFRESH_ERROR = 1000; // ms
const PROGRESS_COMPLETE_TRAIN = 'training complete';
const PROGRESS_MAP_TRAIN = {
    'generating training data': 1,
    'read and resize complete': 10,
    'beginning passthrough of training set': 15,
    'beginning passthrough of testing set': 20,
    'epoch': 20,
    'training complete': 100, // force complete
};
const PROGRESS_COMPLETE_PREDICT = 'image output complete';
const PROGRESS_MAP_PREDICT = {
    'loading model': 1,
    'obtaining images': 10,
    'read and resize complete': 20,
    'beginning xception download': 30,
    'beginning passthrough of images through xception': 50,
    'beginning passthrough of images through trained model': 70,
    'beginning image output': 90,
    'image output complete': 100, // force complete
};

/**
 * Load current train results from server 
 */
const loadTrainResults= async () => {
    let completedMessage = document.getElementById('completed-message');
    let refresh = true;
    let url = '/results/train';    
    try {
        let response = await fetch(url);
        let body = await response.json();
        let logs = body.logs || [];
        if (logs.length > 0) {
            updateTrainProgress('progress-bar-1', logs);        
            document.getElementById('logs').innerHTML = logs.join('');
            let lastLine = logs.length > 0 ? logs[logs.length-1].trim().toLowerCase() : '';            
            if (lastLine.startsWith(PROGRESS_COMPLETE_TRAIN)) {                
                if (body.model_list) {
                    let table = document.getElementById('model-table')
                    body.model_list.forEach((model) => {
                        let tr = document.createElement('tr');
                        for (let key in model) {
                            let td = document.createElement('td');
                            td.innerHTML = model[key];
                            tr.appendChild(td);
                        }
                        table.appendChild(tr);
                    })
                }
                completedMessage.classList.remove('hidden');
                refresh = false;
            }    
        }         
    } catch (e) {
        console.error(e);
    }

    if (refresh === true) {
        completedMessage.classList.add('hidden');
        setTimeout(loadTrainResults, LOG_REFRESH);
    }
}

/**
 * Load current test results from server 
 */
const loadPredictResults = async () => {
    let completedMessage = null;    
    let refresh = true;
    let url = '/results/test';        
    try {
        let response = await fetch(url);
        let body = await response.json();
        let logs = body.logs || [];
        if (logs.length > 0) {
            // determine completed message by first line of logs
            let firstLine = logs[0].split('=')
            if (firstLine[0] === 'images_dir_path') {
                let imagesDirPath = firstLine[1].trim();
                if (imagesDirPath === 'temp') {
                    completedMessage =  document.getElementById('completed-message-images');
                } else {
                    completedMessage =  document.getElementById('completed-message-path');
                    document.getElementsByClassName('output-path')[0].innerHTML = imagesDirPath;
                }
            }            
            updatePredictProgress('progress-bar-1', logs);
            document.getElementById('logs').innerHTML = logs.join('');
            let lastLine = logs.length > 0 ? logs[logs.length-1].trim().toLowerCase() : '';
            if (lastLine.startsWith(PROGRESS_COMPLETE_PREDICT)) {
                completedMessage.classList.remove('hidden');
                refresh = false;
            }
        }

    } catch (e) {
        console.error(e);
        setTimeout(loadPredictResults, LOG_REFRESH_ERROR);
    }
    if (refresh === true) {            
        if (completedMessage) completedMessage.classList.add('hidden');
        setTimeout(loadPredictResults, LOG_REFRESH);
    }

}


/**
 * Update training progress bar based on logs 
 **/
const updateTrainProgress = (progressBarId, logs) => {
    if (!logs || logs.length <= 0) return false;
    let totalEpoch = parseInt(logs[0].split('=')[1]);
    let epochProgress = 70 / totalEpoch;
    let lastLine = '';
    logs.forEach((log) => {
        for (let key in PROGRESS_MAP_TRAIN) {
            log = log.toLowerCase();
            if(log.startsWith(key)) {
                lastLine = log;
                break;
            }
        }        
    });

    if (lastLine.startsWith('epoch')) {
        let lastEpoch = parseInt(lastLine.split('/')[1]);
        setProgressBar(progressBarId, PROGRESS_MAP_TRAIN['epoch'] + lastEpoch * epochProgress);
    } else {
        for (let key in PROGRESS_MAP_TRAIN) {
            if(lastLine.startsWith(key)) {
                setProgressBar(progressBarId, PROGRESS_MAP_TRAIN[key]);
                break;
            }
        }        
    }
}


/**
 * Update testing progress bar based on logs 
 **/
const updatePredictProgress = (progressBarId, logs) => {
    if (!logs || logs.length <= 0) return false;

    let lastLine = '';
    logs.forEach((log, index) => {
        for (let key in PROGRESS_MAP_PREDICT) {
            log = log.toLowerCase();
            if(log.startsWith(key)) {
                lastLine = log;
                break;
            }
        }        
    });

    for (let key in PROGRESS_MAP_PREDICT) {
        if(lastLine.startsWith(key)) {
            setProgressBar(progressBarId, PROGRESS_MAP_PREDICT[key]);
            break;
        }
    }        
}


/**
 * Set progress bar {id} to {pct}% width
 */
const setProgressBar = (id, pct) => {
    let el = document.getElementById(id);    
    pct = pct < 0 ? 0 : pct;
    pct = pct > 100 ? 100 : pct;
    el.style.width = `${pct}%`;
    el.innerHTML = `${pct}%`;
}
