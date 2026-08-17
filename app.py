from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
from datetime import datetime, timedelta
import logging
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Enhanced therapy types with VR-specific techniques and goals
THERAPY_TYPES = {
    'anxiety': {
        'description': 'VR-enhanced anxiety therapy to manage and reduce anxiety symptoms',
        'techniques': [
            {
                'name': 'VR exposure therapy in controlled environments',
                'description': 'Gradual exposure to anxiety-provoking situations in safe virtual environments',
                'week': 'early'
            },
            {
                'name': 'Virtual mindfulness and meditation spaces',
                'description': 'Guided meditation in calming virtual environments',
                'week': 'early'
            },
            {
                'name': 'VR breathing exercises with visual feedback',
                'description': 'Interactive breathing exercises with visual cues for anxiety management',
                'week': 'middle'
            },
            {
                'name': 'Virtual safe space creation and practice',
                'description': 'Creating and practicing in personalized calming virtual environments',
                'week': 'middle'
            },
            {
                'name': 'VR cognitive restructuring scenarios',
                'description': 'Challenging anxious thoughts through immersive scenarios',
                'week': 'late'
            }
        ],
        'goals': 'Reduce anxiety symptoms and develop effective coping strategies in immersive environments',
        'duration': (8, 12),
        'sessions_per_week': 2,
        'vr_requirements': {
            'headset': True,
            'controllers': True,
            'room_scale': False
        }
    },
    'depression': {
        'description': 'VR-enhanced depression treatment focusing on mood improvement',
        'techniques': [
            {
                'name': 'VR behavioral activation environments',
                'description': 'Engaging in positive activities in virtual settings',
                'week': 'early'
            },
            {
                'name': 'Virtual social interaction practice',
                'description': 'Practicing social skills in safe virtual environments',
                'week': 'early'
            },
            {
                'name': 'VR mood tracking and visualization',
                'description': 'Tracking and visualizing mood patterns in VR',
                'week': 'middle'
            },
            {
                'name': 'Virtual achievement and goal-setting spaces',
                'description': 'Setting and achieving goals in immersive environments',
                'week': 'middle'
            },
            {
                'name': 'VR mindfulness and relaxation environments',
                'description': 'Practicing mindfulness in calming virtual spaces',
                'week': 'late'
            }
        ],
        'goals': 'Improve mood through immersive experiences and virtual social engagement',
        'duration': (10, 12),
        'sessions_per_week': 2,
        'vr_requirements': {
            'headset': True,
            'controllers': True,
            'room_scale': False
        }
    },
    'ptsd': {
        'description': 'VR-enhanced trauma-focused therapy for processing traumatic experiences',
        'techniques': [
            {
                'name': 'VR exposure therapy with controlled triggers',
                'description': 'Gradual exposure to trauma-related stimuli in safe virtual environments',
                'week': 'early'
            },
            {
                'name': 'Virtual safe space creation and practice',
                'description': 'Creating and practicing in personalized safe virtual environments',
                'week': 'early'
            },
            {
                'name': 'VR EMDR with visual stimuli',
                'description': 'Eye Movement Desensitization and Reprocessing in virtual settings',
                'week': 'middle'
            },
            {
                'name': 'Virtual grounding exercises',
                'description': 'Practicing grounding techniques in immersive environments',
                'week': 'middle'
            },
            {
                'name': 'VR narrative exposure therapy',
                'description': 'Processing traumatic memories through virtual storytelling',
                'week': 'late'
            }
        ],
        'goals': 'Process traumatic memories in controlled virtual environments',
        'duration': (12, 16),
        'sessions_per_week': 2,
        'vr_requirements': {
            'headset': True,
            'controllers': True,
            'room_scale': True
        }
    },
    'social_anxiety': {
        'description': 'VR-enhanced social anxiety treatment with virtual social scenarios',
        'techniques': [
            {
                'name': 'VR public speaking practice',
                'description': 'Practicing public speaking in virtual environments',
                'week': 'early'
            },
            {
                'name': 'Virtual social interaction simulations',
                'description': 'Practicing social interactions in various virtual scenarios',
                'week': 'early'
            },
            {
                'name': 'VR group therapy environments',
                'description': 'Participating in virtual group therapy sessions',
                'week': 'middle'
            },
            {
                'name': 'Virtual job interview practice',
                'description': 'Practicing job interviews in virtual settings',
                'week': 'middle'
            },
            {
                'name': 'VR social skills training scenarios',
                'description': 'Learning and practicing social skills in immersive environments',
                'week': 'late'
            }
        ],
        'goals': 'Improve social confidence through virtual social interaction practice',
        'duration': (8, 10),
        'sessions_per_week': 2,
        'vr_requirements': {
            'headset': True,
            'controllers': True,
            'room_scale': True
        }
    },
    'phobias': {
        'description': 'VR-enhanced phobia treatment using immersive exposure therapy',
        'techniques': [
            {
                'name': 'VR systematic desensitization',
                'description': 'Gradual exposure to phobic stimuli in virtual environments',
                'week': 'early'
            },
            {
                'name': 'Virtual exposure scenarios',
                'description': 'Controlled exposure to phobic situations in VR',
                'week': 'early'
            },
            {
                'name': 'VR relaxation techniques with visual feedback',
                'description': 'Learning relaxation techniques with visual guidance',
                'week': 'middle'
            },
            {
                'name': 'Virtual safe practice environments',
                'description': 'Practicing coping strategies in safe virtual settings',
                'week': 'middle'
            },
            {
                'name': 'VR cognitive restructuring with immersive scenarios',
                'description': 'Challenging phobic thoughts through virtual experiences',
                'week': 'late'
            }
        ],
        'goals': 'Reduce fear response through controlled virtual exposure',
        'duration': (6, 8),
        'sessions_per_week': 2,
        'vr_requirements': {
            'headset': True,
            'controllers': True,
            'room_scale': True
        }
    },
    'stress': {
        'description': 'VR-enhanced stress management with immersive relaxation techniques',
        'techniques': [
            {
                'name': 'VR mindfulness meditation environments',
                'description': 'Practicing mindfulness in calming virtual spaces',
                'week': 'early'
            },
            {
                'name': 'Virtual nature relaxation spaces',
                'description': 'Relaxing in peaceful virtual natural environments',
                'week': 'early'
            },
            {
                'name': 'VR breathing exercises with visual guidance',
                'description': 'Learning breathing techniques with visual feedback',
                'week': 'middle'
            },
            {
                'name': 'Virtual stress reduction scenarios',
                'description': 'Practicing stress management in various virtual situations',
                'week': 'middle'
            },
            {
                'name': 'VR relaxation training environments',
                'description': 'Learning and practicing relaxation techniques in VR',
                'week': 'late'
            }
        ],
        'goals': 'Develop stress management skills in immersive virtual environments',
        'duration': (6, 8),
        'sessions_per_week': 1,
        'vr_requirements': {
            'headset': True,
            'controllers': False,
            'room_scale': False
        }
    }
}

# Condition detection keywords
CONDITION_KEYWORDS = {
    'anxiety': ['anxiety', 'anxious', 'panic', 'worry', 'nervous', 'fearful'],
    'depression': ['depression', 'depressed', 'sad', 'hopeless', 'empty', 'worthless'],
    'ptsd': ['ptsd', 'trauma', 'flashback', 'nightmare', 'traumatic', 'abuse'],
    'social_anxiety': ['social anxiety', 'shy', 'awkward', 'socially anxious', 'public speaking'],
    'phobias': ['phobia', 'afraid of', 'fear of', 'scared of', 'terrified of'],
    'stress': ['stress', 'stressed', 'overwhelmed', 'burnout', 'pressure']
}

def detect_condition(message):
    """Detect the primary condition based on the message content"""
    message = message.lower()
    condition_scores = {condition: 0 for condition in CONDITION_KEYWORDS.keys()}
    
    for condition, keywords in CONDITION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message:
                condition_scores[condition] += 1
    
    # Get the condition with the highest score
    max_score = max(condition_scores.values())
    if max_score > 0:
        return max(condition_scores.items(), key=lambda x: x[1])[0]
    return 'anxiety'  # Default to anxiety if no clear condition is detected

def generate_schedule(trauma_details):
    """Generate a personalized VR therapy schedule based on the detected condition"""
    logger.debug(f"Generating schedule for: {trauma_details}")
    
    # Detect the primary condition
    condition = detect_condition(trauma_details)
    therapy_info = THERAPY_TYPES[condition]
    
    # Determine number of weeks based on condition
    min_weeks, max_weeks = therapy_info['duration']
    num_weeks = random.randint(min_weeks, max_weeks)
    sessions_per_week = therapy_info['sessions_per_week']
    
    schedule = []
    current_date = datetime.now()
    
    # Define therapy descriptions based on condition and stage
    therapy_descriptions = {
        'phobias': {
            'early': [
                'Initial VR exposure therapy focusing on gradual desensitization',
                'Beginning stages of virtual exposure therapy',
                'Introduction to VR-based phobia treatment'
            ],
            'middle': [
                'Progressive VR exposure therapy with controlled scenarios',
                'Advanced virtual exposure sessions with increased intensity',
                'Structured VR desensitization therapy'
            ],
            'late': [
                'Final stages of VR exposure therapy with complex scenarios',
                'Consolidation of VR-based phobia treatment',
                'Advanced virtual exposure with real-world applications'
            ]
        }
    }
    
    for week in range(num_weeks):
        week_schedule = {
            'description': '',
            'sessions': [],
            'vr_requirements': therapy_info['vr_requirements']
        }
        
        # Generate week description based on progress
        if week == 0:
            week_schedule['description'] = f"Initial VR assessment and introduction to {condition} treatment"
        elif week == num_weeks - 1:
            week_schedule['description'] = "Final week focusing on consolidation and relapse prevention in VR"
        else:
            progress = (week + 1) / num_weeks
            if progress < 0.3:
                week_schedule['description'] = f"Early stage focusing on VR-based understanding of {condition} and initial coping strategies"
            elif progress < 0.7:
                week_schedule['description'] = "Middle stage focusing on active VR treatment and skill development"
            else:
                week_schedule['description'] = "Later stage focusing on application and maintenance of VR-acquired skills"
        
        # Generate sessions for the week
        for session in range(sessions_per_week):
            # Select appropriate techniques based on the week's stage
            if week == 0:
                stage = 'early'
            elif week == num_weeks - 1:
                stage = 'late'
            else:
                progress = (week + 1) / num_weeks
                if progress < 0.3:
                    stage = 'early'
                elif progress < 0.7:
                    stage = 'middle'
                else:
                    stage = 'late'
            
            # Filter techniques for the current stage
            stage_techniques = [t for t in therapy_info['techniques'] if t['week'] == stage]
            technique = random.choice(stage_techniques)
            
            # Calculate session date
            session_date = current_date + timedelta(days=session*3 + week*7)
            
            # Select appropriate therapy description based on condition and stage
            if condition in therapy_descriptions:
                therapy_description = random.choice(therapy_descriptions[condition][stage])
            else:
                therapy_description = therapy_info['description']
            
            week_schedule['sessions'].append({
                'day': session_date.strftime('%A, %B %d'),
                'therapy': therapy_description,
                'technique': technique['name'],
                'technique_description': technique['description'],
                'vr_setup': {
                    'required_equipment': list(filter(lambda x: therapy_info['vr_requirements'][x], 
                                                    ['headset', 'controllers', 'room_scale'])),
                    'estimated_duration': '45-60 minutes',
                    'comfort_level': 'Beginner' if week < 2 else 'Intermediate' if week < num_weeks - 2 else 'Advanced'
                }
            })
        
        schedule.append(week_schedule)
    
    return schedule, condition

@app.route('/generate-schedule', methods=['POST'])
def generate_therapy_schedule():
    try:
        logger.debug("Received request to generate schedule")
        data = request.get_json()
        logger.debug(f"Request data: {data}")
        
        if not data:
            logger.error("No data received in request")
            return jsonify({
                'error': 'No data received'
            }), 400
            
        trauma_details = data.get('trauma_details', '')
        
        if not trauma_details:
            logger.error("No trauma details provided")
            return jsonify({
                'error': 'Please provide trauma details'
            }), 400
        
        schedule, condition = generate_schedule(trauma_details)
        logger.debug(f"Generated schedule for {condition}: {schedule}")
        
        # Generate personalized response based on the condition
        response_message = f"I've analyzed your situation and detected {condition}. "
        response_message += f"I've created a personalized {len(schedule)}-week VR therapy schedule. "
        response_message += "The schedule is designed to address"
        ""
        " your specific needs using immersive VR experiences. "
        response_message += "Each session builds upon the previous ones to ensure steady progress in your recovery journey. "
        response_message += f"Required VR equipment: {', '.join(schedule[0]['vr_requirements'].keys())}."
        
        return jsonify({
            'message': response_message,
            'schedule': schedule,
            'condition': condition
        })
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/schedule_sessions', methods=['POST'])
def schedule_sessions():
    try:
        data = request.get_json()
        dates = data.get('dates', [])
        trauma_details = data.get('trauma_details', '')

        if not dates or not trauma_details:
            return jsonify({
                'success': False, 
                'error': 'Missing required information. Please provide both dates and trauma details.'
            })

        # Determine session type based on trauma details
        session_type = determine_session_type(trauma_details)
        
        # Generate sessions for each selected date
        schedule = []
        for date in dates:
            # Generate session details
            session = {
                'date': date,
                'type': session_type,
                'description': generate_session_description(session_type, trauma_details),
                'duration': '60 minutes',  # Standard session duration
                'vr_requirements': THERAPY_TYPES[get_condition_key(session_type)]['vr_requirements']
            }
            schedule.append(session)

        return jsonify({
            'success': True,
            'schedule': schedule
        })

    except Exception as e:
        logger.error(f"Error scheduling sessions: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'Failed to schedule sessions'
        })

def get_condition_key(session_type):
    """Map session type to condition key"""
    type_to_condition = {
        'Exposure Therapy': 'anxiety',
        'Cognitive Behavioral Therapy': 'depression',
        'Trauma-Focused Therapy': 'ptsd',
        'General Therapy': 'anxiety'  # Default to anxiety for general therapy
    }
    return type_to_condition.get(session_type, 'anxiety')

def determine_session_type(trauma_details):
    # Analyze trauma details to determine appropriate session type
    trauma_details = trauma_details.lower()
    
    if any(word in trauma_details for word in ['anxiety', 'panic', 'stress']):
        return 'Exposure Therapy'
    elif any(word in trauma_details for word in ['depression', 'sad', 'hopeless']):
        return 'Cognitive Behavioral Therapy'
    elif any(word in trauma_details for word in ['ptsd', 'trauma', 'flashback']):
        return 'Trauma-Focused Therapy'
    else:
        return 'General Therapy'

def generate_session_description(session_type, trauma_details):
    descriptions = {
        'Exposure Therapy': 'Gradual exposure to anxiety-provoking situations in a safe VR environment',
        'Cognitive Behavioral Therapy': 'Identifying and challenging negative thought patterns through VR scenarios',
        'Trauma-Focused Therapy': 'Processing traumatic memories in a controlled VR environment',
        'General Therapy': 'General therapeutic support and guidance in a VR setting'
    }
    return descriptions.get(session_type, 'Personalized therapy session in VR environment')

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True, port=5000) 
    app.run(debug=True, port=5000) 