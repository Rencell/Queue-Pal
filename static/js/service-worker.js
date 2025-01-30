class NotificationAPI {
    static requestPermission() {
        if (!('Notification' in window)) {
            console.error('This browser does not support desktop notifications.');
            return;
        }
        Notification.requestPermission().then(permission => {
            if (permission !== 'granted') {
                console.warn('Notification permission denied.');
            }
        });
    }

    static send(title, options = {}) {
        if (!('Notification' in window)) {
            console.error('This browser does not support desktop notifications.');
            return;
        }

        if (Notification.permission === 'granted') {
            let notification = new Notification(title, options);
            if (options.onclick) {
                notification.onclick = options.onclick;
            }
            return notification;
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    let notification = new Notification(title, options);
                    if (options.onclick) {
                        notification.onclick = options.onclick;
                    }
                    return notification;
                }
            });
        }
    }
}

// Usage Example:
// Request permission when the app starts
NotificationAPI.requestPermission();


NotificationAPI.send('Your turn!', {
    body: 'It is your turn now, go to the counter',
    icon: notificationIcon,
    onclick: () => {
        window.focus();
        console.log('Notification clicked!');
    }
});

