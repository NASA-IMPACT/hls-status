const formatDate = timestamp => {
    const date = new Date(timestamp);
    const options = { timeZone: 'UTC', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
    const formattedDate = date.toLocaleString('en-US', options);
    const timezone = 'UTC'; // Specify the timezone here

    return `${formattedDate} (${timezone})`;
  };

export default formatDate;