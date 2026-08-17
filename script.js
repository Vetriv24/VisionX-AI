document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const scheduleContainer = document.getElementById('scheduleContainer');
    const scheduleContent = document.getElementById('scheduleContent');

    // Store the original schedule
    let originalSchedule = null;

    // Initialize calendar
    let selectedDates = [];
    const calendar = flatpickr("#calendar", {
        mode: "multiple",
        dateFormat: "Y-m-d",
        minDate: "today",
        maxDate: new Date().fp_incr(90), // Allow scheduling up to 90 days in advance
        onChange: function(selectedDatesArray, dateStr) {
            selectedDates = selectedDatesArray;
        }
    });

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, 'user');
        userInput.value = '';

        try {
            const response = await fetch('http://localhost:5000/generate-schedule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ trauma_details: message })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error');
            }

            const data = await response.json();
            
            // Add AI response to chat
            addMessage(data.message, 'ai');
            
            // Store and display the generated schedule
            if (data.schedule) {
                originalSchedule = data.schedule;
                displaySchedule(data.schedule);
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage(`Error: ${error.message || 'Failed to process your request. Please make sure the backend server is running.'}`, 'system');
        }
    }

    // Handle schedule button click
    document.getElementById('scheduleButton').addEventListener('click', async function() {
        if (!originalSchedule) {
            addMessage('Please describe your trauma or mental health concerns first to generate a therapy schedule.', 'system');
            return;
        }

        if (selectedDates.length === 0) {
            addMessage('Please select at least one date for your therapy sessions.', 'system');
            return;
        }

        // Sort selected dates to ensure they're in chronological order
        selectedDates.sort((a, b) => a - b);

        // Get all sessions from the original schedule
        const allSessions = [];
        originalSchedule.forEach(week => {
            week.sessions.forEach(session => {
                allSessions.push({
                    therapy: session.therapy,
                    technique: session.technique,
                    technique_description: session.technique_description
                });
            });
        });

        // Create new schedule with only selected dates
        const newSchedule = selectedDates.map((date, index) => {
            if (index < allSessions.length) {
                // Format date to YYYY-MM-DD without timezone adjustments
                const formattedDate = date.getFullYear() + '-' + 
                    String(date.getMonth() + 1).padStart(2, '0') + '-' + 
                    String(date.getDate()).padStart(2, '0');
                
                return {
                    date: formattedDate,
                    type: allSessions[index].therapy,
                    description: allSessions[index].technique_description,
                    duration: '60 minutes'
                };
            }
            return null;
        }).filter(session => session !== null);

        // Clear the original schedule display
        scheduleContent.innerHTML = '';

        // Display only the sessions on selected dates
        displaySelectedDatesSchedule(newSchedule);
        addMessage('Your therapy sessions have been scheduled on your selected dates!', 'system');
    });

    // Function to display schedule for selected dates
    function displaySelectedDatesSchedule(schedule) {
        const scheduleContent = document.getElementById('scheduleContent');
        scheduleContent.innerHTML = '';

        if (!schedule || schedule.length === 0) {
            scheduleContent.innerHTML = '<p class="no-sessions">No sessions scheduled. Please select dates and try again.</p>';
            return;
        }

        // Create a container for the rescheduled sessions
        const rescheduledContainer = document.createElement('div');
        rescheduledContainer.className = 'rescheduled-sessions';

        schedule.forEach(session => {
            const sessionElement = document.createElement('div');
            sessionElement.className = 'session-item';
            sessionElement.innerHTML = `
                <div class="session-header">
                    <h4>Session on ${formatDate(session.date)}</h4>
                </div>
                <div class="session-details">
                    <p class="therapy-type"><strong>Type:</strong> ${session.type}</p>
                    <p class="session-description">${session.description}</p>
                    <p class="session-duration"><strong>Duration:</strong> ${session.duration}</p>
                </div>
            `;
            rescheduledContainer.appendChild(sessionElement);
        });

        scheduleContent.appendChild(rescheduledContainer);
    }

    function rescheduleSessions(originalSchedule, selectedDates) {
        const allSessions = [];
        originalSchedule.forEach(week => {
            week.sessions.forEach(session => {
                allSessions.push({
                    therapy: session.therapy,
                    technique: session.technique,
                    technique_description: session.technique_description
                });
            });
        });

        // Match sessions to selected dates
        return selectedDates.map((date, index) => {
            const sessionIndex = index % allSessions.length;
            return {
                date: date.toISOString().split('T')[0],
                ...allSessions[sessionIndex],
                duration: '60 minutes'
            };
        });
    }

    function displayRescheduledSessions(sessions) {
        const scheduleContent = document.getElementById('scheduleContent');
        scheduleContent.innerHTML = '';

        sessions.forEach(session => {
            const sessionElement = document.createElement('div');
            sessionElement.className = 'session-item';
            sessionElement.innerHTML = `
                <div class="session-header">
                    <h4>Session on ${formatDate(session.date)}</h4>
                </div>
                <div class="session-details">
                    <p class="therapy-type">${session.therapy}</p>
                    <p class="technique"><strong>Technique:</strong> ${session.technique}</p>
                    <p class="technique-description">${session.technique_description}</p>
                    <p class="session-duration"><strong>Duration:</strong> ${session.duration}</p>
                </div>
            `;
            scheduleContent.appendChild(sessionElement);
        });
    }

    function displaySchedule(schedule) {
        scheduleContent.innerHTML = '';
        schedule.forEach((week, index) => {
            const weekDiv = document.createElement('div');
            weekDiv.className = 'week-schedule';
            
            // Create week header with description
            const weekHeader = document.createElement('div');
            weekHeader.className = 'week-header';
            weekHeader.innerHTML = `
                <h3>Week ${index + 1}</h3>
                <p class="week-description">${week.description}</p>
            `;
            weekDiv.appendChild(weekHeader);
            
            // Create sessions list
            const sessionsList = document.createElement('div');
            sessionsList.className = 'sessions-list';
            
            week.sessions.forEach(session => {
                const sessionDiv = document.createElement('div');
                sessionDiv.className = 'session-item';
                sessionDiv.innerHTML = `
                    <div class="session-header">
                        <strong>${session.day}</strong>
                    </div>
                    <div class="session-details">
                        <p class="therapy-type">${session.therapy}</p>
                        <p class="technique"><strong>Technique:</strong> ${session.technique}</p>
                        <p class="technique-description">${session.technique_description}</p>
                    </div>
                `;
                sessionsList.appendChild(sessionDiv);
            });
            
            weekDiv.appendChild(sessionsList);
            scheduleContent.appendChild(weekDiv);
        });
    }

    // Helper function to format date
    function formatDate(dateString) {
        const [year, month, day] = dateString.split('-');
        const date = new Date(year, month - 1, day);
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }

    // Function to add messages to chat
    function addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});