# Requirements Document: Awaaz

## Introduction

Awaaz is an AI-powered government scheme and document facilitation assistant designed for Indian citizens, particularly those with low digital literacy in rural and semi-urban areas. The system provides voice-first, WhatsApp-based assistance to help users discover government schemes, verify documents, complete applications, and receive remedial support for missing or expired documents.

## Glossary

- **Awaaz_System**: The complete AI-powered assistant including voice processing, document verification, and application guidance
- **Voice_Processor**: Component handling speech-to-text (ASR), text-to-speech (TTS), and translation via Bhashini
- **Document_Verifier**: Component performing OCR and validation of uploaded documents
- **Scheme_Matcher**: Component matching user problems to relevant government schemes
- **Application_Assistant**: Component guiding users through application completion
- **Remedial_Engine**: Component providing guidance for missing/expired documents
- **Profile_Manager**: Component managing user data and conversation history
- **WhatsApp_Interface**: Integration layer with WhatsApp Business API
- **User**: Indian citizen interacting with the system
- **Session**: A continuous conversation between User and Awaaz_System
- **Document**: Government-issued identification or proof (Aadhaar, PAN, address proof, etc.)
- **Scheme**: Government welfare program or service
- **Bhashini**: Government of India's language translation platform

## Requirements

### Requirement 1: Voice-First Conversational Interface

**User Story:** As a user with low digital literacy, I want to interact primarily through voice notes, so that I can use the system without typing.

#### Acceptance Criteria

1. WHEN a User sends a voice note via WhatsApp, THE Voice_Processor SHALL transcribe it to text within 5 seconds
2. WHEN the Voice_Processor transcribes voice input, THE Awaaz_System SHALL process the request and generate a response
3. WHEN the Awaaz_System generates a response, THE Voice_Processor SHALL convert it to speech in the User's language
4. WHEN a User sends text input, THE Awaaz_System SHALL process it equivalently to voice input
5. WHEN the Awaaz_System requires confirmation, THE WhatsApp_Interface SHALL present button-based options to minimize typing
6. WHEN voice processing fails, THE Awaaz_System SHALL request the User to resend the voice note with a clear error message

### Requirement 2: Multilingual Support

**User Story:** As a user who speaks a regional Indian language, I want the system to understand and respond in my language, so that I can communicate naturally.

#### Acceptance Criteria

1. WHEN a User sends their first message in a Session, THE Voice_Processor SHALL detect the language automatically
2. WHEN the language is detected, THE Awaaz_System SHALL maintain that language throughout the Session
3. THE Voice_Processor SHALL support Hindi, English, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and Assamese
4. WHEN generating responses, THE Awaaz_System SHALL use simple, colloquial phrasing appropriate for the detected language
5. WHEN translation is required, THE Voice_Processor SHALL use Bhashini API for accurate regional translation
6. IF language detection fails, THEN THE Awaaz_System SHALL default to Hindi and allow User to specify preferred language

### Requirement 3: Problem Understanding and Scheme Discovery

**User Story:** As a user seeking government assistance, I want to describe my problem in my own words, so that the system can find relevant schemes for me.

#### Acceptance Criteria

1. WHEN a User describes a problem, THE Scheme_Matcher SHALL identify the most relevant government scheme
2. WHEN multiple schemes are potentially relevant, THE Scheme_Matcher SHALL select the single most appropriate scheme based on User context
3. WHEN a scheme is identified, THE Awaaz_System SHALL explain the scheme in everyday spoken language
4. WHEN clarification is needed, THE Awaaz_System SHALL ask no more than 3 clarifying questions
5. WHEN explaining a scheme, THE Awaaz_System SHALL include eligibility criteria, benefits, and required documents
6. THE Scheme_Matcher SHALL use structured JSON data from government portals for scheme information

### Requirement 4: Document Verification

**User Story:** As a user applying for a government scheme, I want to verify my documents are valid and readable, so that my application is not rejected.

#### Acceptance Criteria

1. WHEN a scheme requires documents, THE Awaaz_System SHALL announce each required document via voice
2. WHEN a User uploads a document image, THE Document_Verifier SHALL perform OCR within 10 seconds
3. WHEN performing OCR, THE Document_Verifier SHALL automatically detect the document type (Aadhaar, PAN, passport, etc.)
4. WHEN a document is processed, THE Document_Verifier SHALL validate name consistency across all uploaded documents
5. WHEN a document is processed, THE Document_Verifier SHALL check image clarity and readability
6. WHEN a document is processed, THE Document_Verifier SHALL extract and validate issue date and expiry date
7. WHEN a document is processed, THE Document_Verifier SHALL verify all required fields are present and legible
8. WHEN validation completes, THE Awaaz_System SHALL provide clear voice feedback on validation status
9. IF a document fails validation, THEN THE Awaaz_System SHALL explain the specific issue in simple language
10. THE Document_Verifier SHALL use OpenCV and Tesseract for OCR processing
11. WHEN processing images, THE Document_Verifier SHALL handle compressed images optimized for low bandwidth

### Requirement 5: Application Assistance

**User Story:** As a user completing a government application, I want step-by-step guidance, so that I can submit a complete and correct application.

#### Acceptance Criteria

1. WHEN an application process begins, THE Application_Assistant SHALL guide the User through each field sequentially
2. WHEN collecting information, THE Application_Assistant SHALL ask one question at a time via voice
3. WHEN a User provides information, THE Application_Assistant SHALL confirm the input before proceeding to the next field
4. WHEN all required information is collected, THE Application_Assistant SHALL summarize the complete application for User confirmation
5. WHEN the application is complete, THE Awaaz_System SHALL indicate submission readiness
6. THE Application_Assistant SHALL pre-fill fields using information from verified documents
7. THE Application_Assistant SHALL pre-fill fields using stored Profile_Manager data when available

### Requirement 6: Remedial Support

**User Story:** As a user with missing or expired documents, I want guidance on how to obtain valid documents, so that I can complete my application.

#### Acceptance Criteria

1. WHEN a required document is missing, THE Remedial_Engine SHALL explain why the document is needed
2. WHEN a document is expired, THE Remedial_Engine SHALL explain the renewal process including office location, required steps, and estimated timeline
3. WHEN an affidavit can substitute for a missing document, THE Remedial_Engine SHALL offer to generate the affidavit
4. WHEN a User agrees to affidavit generation, THE Remedial_Engine SHALL create a properly formatted affidavit PDF
5. WHEN providing remedial guidance, THE Awaaz_System SHALL explain submission steps clearly via voice
6. THE Remedial_Engine SHALL use Jinja2 templates and ReportLab for PDF generation

### Requirement 7: User Profile Management

**User Story:** As a returning user, I want the system to remember my information, so that I don't have to provide the same details repeatedly.

#### Acceptance Criteria

1. WHEN a User interacts with the system, THE Profile_Manager SHALL store User details progressively
2. WHEN a User returns, THE Profile_Manager SHALL retrieve stored profile information
3. THE Profile_Manager SHALL maintain conversation history for each User
4. WHEN collecting information, THE Awaaz_System SHALL use stored profile data to avoid redundant questions
5. THE Profile_Manager SHALL store verified document information for future reference
6. THE Profile_Manager SHALL use SQLite for data persistence

### Requirement 8: WhatsApp Integration

**User Story:** As a user with a basic smartphone, I want to access the system through WhatsApp, so that I don't need to install additional apps.

#### Acceptance Criteria

1. THE WhatsApp_Interface SHALL integrate with WhatsApp Business API
2. WHEN a User sends a message, THE WhatsApp_Interface SHALL receive and forward it to the Awaaz_System within 2 seconds
3. WHEN the Awaaz_System generates a response, THE WhatsApp_Interface SHALL deliver it via WhatsApp
4. WHEN sending voice responses, THE WhatsApp_Interface SHALL deliver audio files in WhatsApp-compatible format
5. WHEN presenting options, THE WhatsApp_Interface SHALL use WhatsApp button templates
6. THE WhatsApp_Interface SHALL handle image uploads for document verification

### Requirement 9: Performance and Optimization

**User Story:** As a user in a rural area with limited internet connectivity, I want the system to work on low bandwidth, so that I can use it despite network constraints.

#### Acceptance Criteria

1. WHEN generating responses, THE Awaaz_System SHALL keep voice messages under 30 seconds
2. WHEN processing documents, THE Document_Verifier SHALL accept compressed images with minimum 150 DPI resolution
3. WHEN sending responses, THE Awaaz_System SHALL prioritize voice summaries over long text messages
4. THE Awaaz_System SHALL respond to User inputs within 10 seconds under normal network conditions
5. WHEN network latency is detected, THE Awaaz_System SHALL provide acknowledgment messages to indicate processing

### Requirement 10: Conversation Flow and User Experience

**User Story:** As a user seeking government assistance, I want clear, task-oriented guidance, so that I can complete my objective efficiently.

#### Acceptance Criteria

1. THE Awaaz_System SHALL maintain a task-oriented conversation flow focused on completing the User's objective
2. THE Awaaz_System SHALL avoid providing unsolicited information or multiple options simultaneously
3. WHEN a User's intent is unclear, THE Awaaz_System SHALL ask specific clarifying questions rather than listing possibilities
4. WHEN completing a task, THE Awaaz_System SHALL provide a clear summary of what was accomplished and next steps
5. THE Awaaz_System SHALL use reassuring and supportive language throughout interactions
6. THE Awaaz_System SHALL never assume User knowledge of government processes or terminology

### Requirement 11: Data Management and Scheme Information

**User Story:** As a system administrator, I want scheme data to be easily updatable, so that the system remains current with government programs.

#### Acceptance Criteria

1. THE Scheme_Matcher SHALL load scheme data from structured JSON files
2. WHEN scheme data is updated, THE Awaaz_System SHALL reflect changes without requiring code modifications
3. THE Awaaz_System SHALL source scheme data from MyGov portal, central government portals, and state government portals
4. WHEN storing scheme data, THE Awaaz_System SHALL normalize information into a consistent structure
5. THE Scheme_Matcher SHALL include scheme eligibility criteria, required documents, benefits, and application process in structured format

### Requirement 12: Error Handling and Reliability

**User Story:** As a user, I want clear guidance when something goes wrong, so that I can continue with my task.

#### Acceptance Criteria

1. WHEN OCR fails to read a document, THE Awaaz_System SHALL request a clearer image with specific guidance
2. WHEN voice transcription fails, THE Awaaz_System SHALL request the User to resend the voice note
3. WHEN the Bhashini API is unavailable, THE Awaaz_System SHALL fall back to English and notify the User
4. WHEN a Session is interrupted, THE Awaaz_System SHALL allow the User to resume from the last completed step
5. WHEN an unexpected error occurs, THE Awaaz_System SHALL provide a helpful error message and suggest next steps
6. THE Awaaz_System SHALL log all errors for system monitoring and improvement
