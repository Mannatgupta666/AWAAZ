# Design Document: Awaaz

## Overview

Awaaz is a voice-first, WhatsApp-based AI assistant that helps Indian citizens navigate government schemes and document verification. The system is designed for users with low digital literacy in rural and semi-urban areas, providing a conversational interface that guides them through discovering schemes, verifying documents, completing applications, and obtaining remedial support.

The architecture follows a modular design with clear separation between voice processing, document verification, scheme matching, application assistance, and remedial support. The system integrates with Bhashini for multilingual support and WhatsApp Business API for messaging.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User (WhatsApp)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   WhatsApp Interface Layer                   │
│  - Message Reception/Delivery                                │
│  - Media Handling (Voice, Images)                            │
│  - Button Templates                                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Conversation Manager                      │
│  - Session Management                                        │
│  - Context Tracking                                          │
│  - Flow Orchestration                                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│    Voice     │   │   Scheme     │   │  Document    │
│  Processor   │   │   Matcher    │   │  Verifier    │
│              │   │              │   │              │
│ - ASR (STT)  │   │ - Problem    │   │ - OCR        │
│ - TTS        │   │   Analysis   │   │ - Type       │
│ - Translation│   │ - Scheme     │   │   Detection  │
│ - Bhashini   │   │   Selection  │   │ - Validation │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Application  │   │  Remedial    │   │   Profile    │
│  Assistant   │   │   Engine     │   │   Manager    │
│              │   │              │   │              │
│ - Field      │   │ - Missing    │   │ - User Data  │
│   Collection │   │   Doc Guide  │   │ - History    │
│ - Pre-fill   │   │ - Affidavit  │   │ - SQLite     │
│ - Validation │   │   Generation │   │   Storage    │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Component Interaction Flow

1. **User Input Flow**: WhatsApp → WhatsApp Interface → Voice Processor (if voice) → Conversation Manager
2. **Processing Flow**: Conversation Manager → Appropriate Component (Scheme Matcher, Document Verifier, etc.)
3. **Response Flow**: Component → Conversation Manager → Voice Processor (TTS) → WhatsApp Interface → User

## Components and Interfaces

### 1. WhatsApp Interface Layer

**Responsibilities:**

- Receive messages (text, voice, images) from WhatsApp Business API
- Send messages (text, voice) to users
- Handle media uploads and downloads
- Present button-based UI elements

**Key Interfaces:**

```python
class WhatsAppInterface:
    def receive_message(webhook_data: dict) -> Message:
        """Process incoming webhook from WhatsApp"""

    def send_text_message(phone_number: str, text: str) -> bool:
        """Send text message to user"""

    def send_voice_message(phone_number: str, audio_data: bytes) -> bool:
        """Send voice message to user"""

    def send_button_message(phone_number: str, text: str, buttons: list[Button]) -> bool:
        """Send message with interactive buttons"""

    def download_media(media_id: str) -> bytes:
        """Download voice note or image from WhatsApp"""
```

**Data Structures:**

```python
@dataclass
class Message:
    phone_number: str
    message_type: MessageType  # TEXT, VOICE, IMAGE, BUTTON_RESPONSE
    content: str | bytes
    timestamp: datetime
    media_id: Optional[str]

@dataclass
class Button:
    id: str
    title: str
```

### 2. Voice Processor

**Responsibilities:**

- Convert voice to text (ASR) using Bhashini
- Convert text to voice (TTS) using Bhashini
- Detect language from input
- Translate between languages if needed

**Key Interfaces:**

```python
class VoiceProcessor:
    def transcribe_voice(audio_data: bytes, language: Optional[str] = None) -> TranscriptionResult:
        """Convert voice to text using Bhashini ASR"""

    def synthesize_speech(text: str, language: str) -> bytes:
        """Convert text to voice using Bhashini TTS"""

    def detect_language(text: str) -> str:
        """Detect language from text input"""

    def translate_text(text: str, source_lang: str, target_lang: str) -> str:
        """Translate text using Bhashini"""
```

**Data Structures:**

```python
@dataclass
class TranscriptionResult:
    text: str
    language: str
    confidence: float
```

### 3. Conversation Manager

**Responsibilities:**

- Maintain session state for each user
- Track conversation context and flow
- Orchestrate component interactions
- Determine next action based on current state

**Key Interfaces:**

```python
class ConversationManager:
    def process_user_input(phone_number: str, message: Message) -> Response:
        """Process user input and generate appropriate response"""

    def get_session(phone_number: str) -> Session:
        """Retrieve or create session for user"""

    def update_session_state(phone_number: str, state: ConversationState) -> None:
        """Update session state"""

    def determine_next_action(session: Session, user_input: str) -> Action:
        """Determine what action to take based on current state"""
```

**Data Structures:**

```python
@dataclass
class Session:
    phone_number: str
    language: str
    state: ConversationState
    context: dict  # Stores current scheme, documents, application data
    history: list[Message]
    created_at: datetime
    updated_at: datetime

class ConversationState(Enum):
    INITIAL = "initial"
    PROBLEM_UNDERSTANDING = "problem_understanding"
    SCHEME_EXPLANATION = "scheme_explanation"
    DOCUMENT_COLLECTION = "document_collection"
    DOCUMENT_VERIFICATION = "document_verification"
    APPLICATION_FILLING = "application_filling"
    REMEDIAL_SUPPORT = "remedial_support"
    COMPLETION = "completion"

@dataclass
class Response:
    text: str
    voice_data: Optional[bytes]
    buttons: Optional[list[Button]]
    requires_input: bool
```

### 4. Scheme Matcher

**Responsibilities:**

- Load and index government scheme data
- Match user problems to relevant schemes
- Provide scheme information in structured format

**Key Interfaces:**

```python
class SchemeMatcher:
    def load_schemes(schemes_directory: str) -> None:
        """Load scheme data from JSON files"""

    def match_problem_to_scheme(problem_description: str, user_context: dict) -> Scheme:
        """Find most relevant scheme for user's problem"""

    def get_scheme_details(scheme_id: str) -> Scheme:
        """Retrieve detailed information about a scheme"""

    def generate_scheme_explanation(scheme: Scheme, language: str) -> str:
        """Generate user-friendly explanation of scheme"""
```

**Data Structures:**

```python
@dataclass
class Scheme:
    id: str
    name: str
    description: str
    eligibility_criteria: list[str]
    required_documents: list[str]
    benefits: list[str]
    application_process: list[str]
    category: str  # education, health, housing, etc.
    target_audience: list[str]
```

### 5. Document Verifier

**Responsibilities:**

- Perform OCR on uploaded document images
- Detect document type automatically
- Validate document fields and consistency
- Check expiry dates and clarity

**Key Interfaces:**

```python
class DocumentVerifier:
    def verify_document(image_data: bytes, expected_type: Optional[str] = None) -> DocumentVerificationResult:
        """Perform OCR and validation on document"""

    def detect_document_type(image_data: bytes) -> str:
        """Automatically detect document type"""

    def extract_fields(image_data: bytes, document_type: str) -> dict:
        """Extract specific fields based on document type"""

    def validate_consistency(documents: list[VerifiedDocument]) -> ConsistencyResult:
        """Check name and other field consistency across documents"""

    def check_image_quality(image_data: bytes) -> QualityResult:
        """Assess if image is clear enough for OCR"""
```

**Data Structures:**

```python
@dataclass
class DocumentVerificationResult:
    document_type: str
    extracted_fields: dict
    is_valid: bool
    validation_errors: list[str]
    expiry_date: Optional[datetime]
    is_expired: bool
    quality_score: float

@dataclass
class VerifiedDocument:
    document_type: str
    fields: dict
    image_data: bytes
    verification_result: DocumentVerificationResult
    uploaded_at: datetime

@dataclass
class ConsistencyResult:
    is_consistent: bool
    inconsistencies: list[str]

@dataclass
class QualityResult:
    is_acceptable: bool
    quality_score: float
    issues: list[str]
```

### 6. Application Assistant

**Responsibilities:**

- Guide users through application form filling
- Collect information conversationally
- Pre-fill fields from verified documents and profile
- Validate collected information

**Key Interfaces:**

```python
class ApplicationAssistant:
    def start_application(scheme: Scheme, verified_documents: list[VerifiedDocument]) -> ApplicationSession:
        """Initialize application filling process"""

    def get_next_field(application_session: ApplicationSession) -> Field:
        """Get next field to collect from user"""

    def collect_field_value(field: Field, user_input: str) -> FieldValue:
        """Process and validate user input for field"""

    def prefill_from_documents(application_session: ApplicationSession, documents: list[VerifiedDocument]) -> None:
        """Pre-fill application fields from verified documents"""

    def generate_summary(application_session: ApplicationSession) -> str:
        """Generate summary of completed application"""
```

**Data Structures:**

```python
@dataclass
class ApplicationSession:
    scheme_id: str
    fields: list[Field]
    collected_values: dict[str, FieldValue]
    current_field_index: int
    is_complete: bool

@dataclass
class Field:
    name: str
    label: str
    field_type: FieldType  # TEXT, NUMBER, DATE, CHOICE
    is_required: bool
    validation_rules: list[str]
    prefill_source: Optional[str]  # document field or profile field

@dataclass
class FieldValue:
    field_name: str
    value: Any
    is_valid: bool
    validation_errors: list[str]
```

### 7. Remedial Engine

**Responsibilities:**

- Provide guidance for missing documents
- Explain document renewal processes
- Generate affidavits and declarations
- Guide users on submission steps

**Key Interfaces:**

```python
class RemedialEngine:
    def generate_missing_document_guidance(document_type: str, user_location: str) -> Guidance:
        """Provide guidance for obtaining missing document"""

    def generate_renewal_guidance(document_type: str, expiry_date: datetime) -> Guidance:
        """Provide guidance for renewing expired document"""

    def can_generate_affidavit(document_type: str) -> bool:
        """Check if affidavit can substitute for document"""

    def generate_affidavit(document_type: str, user_details: dict) -> bytes:
        """Generate affidavit PDF"""

    def explain_submission_process(scheme: Scheme, completed_documents: list[str]) -> str:
        """Explain how to submit application"""
```

**Data Structures:**

```python
@dataclass
class Guidance:
    document_type: str
    steps: list[str]
    office_location: Optional[str]
    estimated_timeline: Optional[str]
    required_items: list[str]
    alternative_options: list[str]
```

### 8. Profile Manager

**Responsibilities:**

- Store and retrieve user profile information
- Maintain conversation history
- Store verified document metadata
- Provide data persistence using SQLite

**Key Interfaces:**

```python
class ProfileManager:
    def get_profile(phone_number: str) -> UserProfile:
        """Retrieve user profile"""

    def update_profile(phone_number: str, updates: dict) -> None:
        """Update user profile information"""

    def store_verified_document(phone_number: str, document: VerifiedDocument) -> None:
        """Store verified document metadata"""

    def get_conversation_history(phone_number: str, limit: int = 50) -> list[Message]:
        """Retrieve conversation history"""

    def add_to_history(phone_number: str, message: Message) -> None:
        """Add message to conversation history"""
```

**Data Structures:**

```python
@dataclass
class UserProfile:
    phone_number: str
    name: Optional[str]
    preferred_language: str
    location: Optional[str]
    verified_documents: list[str]  # document types
    profile_data: dict  # flexible storage for collected information
    created_at: datetime
    updated_at: datetime
```

## Data Models

### Database Schema (SQLite)

```sql
-- Users table
CREATE TABLE users (
    phone_number TEXT PRIMARY KEY,
    name TEXT,
    preferred_language TEXT NOT NULL,
    location TEXT,
    profile_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    state TEXT NOT NULL,
    context JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (phone_number) REFERENCES users(phone_number)
);

-- Messages table (conversation history)
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    message_type TEXT NOT NULL,
    content TEXT,
    is_from_user BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (phone_number) REFERENCES users(phone_number)
);

-- Verified documents table
CREATE TABLE verified_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    document_type TEXT NOT NULL,
    extracted_fields JSON,
    verification_status TEXT NOT NULL,
    expiry_date TIMESTAMP,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (phone_number) REFERENCES users(phone_number)
);

-- Application sessions table
CREATE TABLE application_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    scheme_id TEXT NOT NULL,
    collected_values JSON,
    is_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (phone_number) REFERENCES users(phone_number)
);
```

### Scheme Data Format (JSON)

```json
{
  "id": "domicile-certificate-maharashtra",
  "name": "Domicile Certificate",
  "state": "Maharashtra",
  "category": "identity",
  "description": "Certificate proving residence in Maharashtra",
  "eligibility_criteria": [
    "Resident of Maharashtra for at least 15 years",
    "Age 18 or above"
  ],
  "required_documents": ["aadhaar", "pan", "address_proof", "passport_photo"],
  "benefits": [
    "Required for state government schemes",
    "Educational institution admissions",
    "Government job applications"
  ],
  "application_process": [
    "Fill application form",
    "Attach required documents",
    "Submit at Tehsil office",
    "Collect certificate in 7-15 days"
  ],
  "target_audience": ["students", "job_seekers", "residents"],
  "application_fields": [
    {
      "name": "full_name",
      "label": "Full Name",
      "type": "text",
      "required": true,
      "prefill_from": "aadhaar.name"
    },
    {
      "name": "duration_of_stay",
      "label": "How long have you lived in Maharashtra?",
      "type": "number",
      "required": true,
      "validation": "minimum_15_years"
    }
  ]
}
```
