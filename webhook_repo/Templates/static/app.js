async function fetchEvents() {
    const res = await fetch('/events');
    const events = await res.json();
    const list = document.getElementById('events-list');
    list.innerHTML = "";

    events.reverse().forEach(event => {
        let text = "";
        if (event.type === "push") {
            text = `${event.author} pushed to ${event.to_branch} on ${event.timestamp}`;
        } else if (event.type === "pull_request") {
            text = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
        } else if (event.type === "merge") {
            text = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
        }
        const li = document.createElement("li");
        li.textContent = text;
        list.appendChild(li);
    });
}

setInterval(fetchEvents, 15000); // Poll every 15 seconds
window.onload = fetchEvents;
