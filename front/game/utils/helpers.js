function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

export { delay, getQueryParam };
