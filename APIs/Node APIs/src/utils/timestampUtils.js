module.exports.convertISOTimestamptoLocalString = function(timestamp) {

    const timestampObj = new Date(timestamp);
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
    };

    const formattedDate = timestampObj.toLocaleString('en-US', options);
    return formattedDate;
}