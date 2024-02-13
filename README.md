# email_service
email_service - tiny wrapper server around smtplib to send emails


## Installation
* Install requirements.txt 
* Run the server: `python3 manage.py runserver`
* update local_settings.py (from example)
* Run the curl:

```commandline

Testing it out via curl
```commandline
curl -X POST \
  http://localhost:8000/email \
  -H 'Content-Type: application/json' \
  -H 'User-Agent: Chrome' \
  -H 'Origin: https://wojciklaw.ca' \
  -d '{"subject": "test email", "from_user": "John Doe", "from_user_email": "jon@doe.com", "message": "Hello, this is a test message"}'
```


## Deploy (Ubuntu)

See provided email_service.service and service.sh files for systemd deployment



## Prevent email spamming

See fail2ban i.e. something like this to ban users abusing the system

```
[nginx-limit-req]
enabled  = true
filter   = nginx-limit-req
action   = iptables-allports[name=nginx-limit-req, protocol=all]
           sendmail-whois[name=nginx-limit-req, dest=you@example.com, sender=fail2ban@example.com]
logpath  = /var/log/nginx/*error.log
maxretry = 30
findtime = 600
bantime  = -1
```


## Nginx proxy pass

```
location /email {
    limit_req_zone $binary_remote_addr zone=blacklist_zone:10m rate=5r/m;
    #limit_req zone=blacklist_zone nodelay;  # No burst
    limit_req zone=blacklist_zone burst=5 nodelay;

    proxy_pass http://localhost:8001/email;
    proxy_pass_request_body on;
    proxy_set_header Content-Length "";

    proxy_pass_header Server;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;

    # Add other proxy settings if needed
}
```