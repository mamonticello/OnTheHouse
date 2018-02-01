function post(url, data, callback)
{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function()
    {
        if (request.readyState == 4)
        {
            if (callback != null)
            {
                var text = request.responseText;
                var response = JSON.parse(text);
                response["_request_url"] = url;
                response["_status"] = request.status;
                callback(response);
            }
        }
    };
    var asynchronous = true;
    request.open("POST", url, asynchronous);
    request.send(data);
}
