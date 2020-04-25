const LOG_REFRESH = 3000; // ms
const LOG_REFRESH_ERROR = 1000; // ms
const PROGRESS_MAP_TRAIN = {
    'generating training data': 1,
    'read and resize complete': 10,
    'beginning passthrough of training set': 15,
    'beginning passthrough of testing set': 20,
    'epoch': 20,
    'training complete': 100, // force complete
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
            if (lastLine.startsWith('training complete')) {                
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
 * Set progress bar {id} to {pct}% width
 */
const setProgressBar = (id, pct) => {
    let el = document.getElementById(id);    
    pct = pct < 0 ? 0 : pct;
    pct = pct > 100 ? 100 : pct;
    el.style.width = `${pct}%`;
    el.innerHTML = `${pct}%`;
}
