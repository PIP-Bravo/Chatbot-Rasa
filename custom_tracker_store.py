# custom_tracker_store.py
from rasa.core.tracker_store import SQLTrackerStore
import csv
import os
import json
from datetime import datetime
from typing import Dict, Any, List

class TimedSQLTrackerStore(SQLTrackerStore):
    def __init__(self, domain, **kwargs):
        super().__init__(domain, **kwargs)
        self.init_response_time_log()
        self.init_confidence_log()
        self.init_pipeline_debug_log()

    def init_response_time_log(self):
        self.log_file = "response_rasa.csv"
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'conversation_id', 'user_message', 
                    'intent', 'confidence', 'bot_response', 'total_response_time_ms', 'coverage'
                ])

    def init_confidence_log(self):
        """File untuk menyimpan confidence scores semua intent"""
        self.confidence_log_file = "all_intent_confidence.csv"
        if not os.path.exists(self.confidence_log_file):
            with open(self.confidence_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'conversation_id', 'user_message',
                    'predicted_intent', 'predicted_confidence', 'intent_ranking_json'
                ])

    def init_pipeline_debug_log(self):
        """File untuk debug proses pipeline"""
        self.debug_log_file = "pipeline_debug.csv"
        if not os.path.exists(self.debug_log_file):
            with open(self.debug_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'conversation_id', 'user_message',
                    'event_types', 'latest_intent', 'latest_action',
                    'fallback_triggered', 'entities_count'
                ])

    def _extract_intent_ranking(self, events: List) -> List[Dict[str, Any]]:
        """Extract intent ranking dari events"""
        for event in reversed(events):
            if hasattr(event, 'type_name') and event.type_name == 'user':
                if hasattr(event, 'intent_ranking') and event.intent_ranking:
                    return event.intent_ranking
                elif hasattr(event, 'intent') and event.intent:
                    # Jika tidak ada ranking, buat ranking sederhana dari intent utama
                    return [{
                        'name': event.intent.get('name', ''),
                        'confidence': event.intent.get('confidence', 0)
                    }]
        return []

    def _extract_all_events_info(self, events: List) -> Dict[str, Any]:
        """Extract informasi dari semua events untuk debugging"""
        event_types = []
        latest_intent = ""
        latest_action = ""
        entities_count = 0
        fallback_triggered = False

        for event in events:
            event_type = event.type_name if hasattr(event, 'type_name') else str(type(event))
            event_types.append(event_type)
            
            if event_type == 'user':
                if hasattr(event, 'intent'):
                    latest_intent = event.intent.get('name', '')
                    if latest_intent in ["nlu_fallback", "out_of_scope"]:
                        fallback_triggered = True
                if hasattr(event, 'entities'):
                    entities_count = len(event.entities)
            
            elif event_type == 'bot':
                if hasattr(event, 'action_name'):
                    latest_action = event.action_name

        return {
            'event_types': event_types,
            'latest_intent': latest_intent,
            'latest_action': latest_action,
            'fallback_triggered': fallback_triggered,
            'entities_count': entities_count
        }

    def _log_confidence_scores(self, tracker, user_event: Dict[str, Any]):
        """Log confidence scores untuk semua intent"""
        intent_ranking = self._extract_intent_ranking(tracker.events)
        
        # Sort intent ranking by confidence (descending)
        sorted_ranking = sorted(intent_ranking, key=lambda x: x.get('confidence', 0), reverse=True)
        
        # Simpan sebagai JSON string untuk kemudahan parsing
        ranking_json = json.dumps(sorted_ranking, ensure_ascii=False)
        
        with open(self.confidence_log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                tracker.sender_id,
                user_event.get('text', ''),
                user_event.get('intent', ''),
                user_event.get('confidence', 0),
                ranking_json
            ])
        
        # Juga buat log terpisah dengan format tabel untuk readability
        self._log_confidence_table(tracker.sender_id, user_event.get('text', ''), sorted_ranking)

    def _log_confidence_table(self, conversation_id: str, user_message: str, intent_ranking: List[Dict]):
        """Log confidence scores dalam format tabel yang mudah dibaca"""
        table_file = "intent_confidence_ranking.csv"
        
        # Cek apakah file sudah ada dan header perlu ditulis
        file_exists = os.path.exists(table_file)
        
        with open(table_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Tulis header jika file baru
            if not file_exists:
                writer.writerow([
                    'timestamp', 'conversation_id', 'user_message',
                    'rank', 'intent_name', 'confidence_score', 'is_predicted'
                ])
            
            # Tulis data ranking
            timestamp = datetime.now().isoformat()
            for i, intent_info in enumerate(intent_ranking):
                is_predicted = "YES" if i == 0 else "NO"
                writer.writerow([
                    timestamp,
                    conversation_id,
                    user_message if i == 0 else "",  # Hanya tulis sekali per message
                    i + 1,
                    intent_info.get('name', ''),
                    f"{intent_info.get('confidence', 0):.6f}",
                    is_predicted
                ])

    def _log_pipeline_debug(self, tracker, user_event: Dict[str, Any]):
        """Log informasi debug untuk proses pipeline"""
        events_info = self._extract_all_events_info(tracker.events)
        
        with open(self.debug_log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                tracker.sender_id,
                user_event.get('text', ''),
                str(events_info['event_types'][-5:]),  # 5 events terakhir
                events_info['latest_intent'],
                events_info['latest_action'],
                events_info['fallback_triggered'],
                events_info['entities_count']
            ])

    def _extract_user_event(self, events: List) -> Dict[str, Any]:
        """Extract user event dengan informasi yang lebih lengkap"""
        for event in reversed(events):
            event_type = event.type_name if hasattr(event, 'type_name') else str(type(event))
            
            if event_type == 'user':
                return {
                    'text': event.text if hasattr(event, 'text') else '',
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else 0,
                    'intent': event.intent.get('name') if hasattr(event, 'intent') and event.intent else '',
                    'confidence': event.intent.get('confidence') if hasattr(event, 'intent') and event.intent else 0,
                    'entities': event.entities if hasattr(event, 'entities') else []
                }
        return {}

    def _extract_bot_event(self, events: List) -> Dict[str, Any]:
        """Extract bot event"""
        for event in reversed(events):
            event_type = event.type_name if hasattr(event, 'type_name') else str(type(event))
            
            if event_type == 'bot':
                return {
                    'text': event.text if hasattr(event, 'text') else '',
                    'timestamp': event.timestamp if hasattr(event, 'timestamp') else 0,
                    'action_name': event.action_name if hasattr(event, 'action_name') else ''
                }
        return {}

    async def save(self, tracker):
        await super().save(tracker)
        
        # Extract events
        user_event = self._extract_user_event(tracker.events)
        bot_event = self._extract_bot_event(tracker.events)
        
        if user_event and bot_event:
            total_response_time = (bot_event.get('timestamp', 0) - user_event.get('timestamp', 0)) * 1000
            is_fallback = user_event.get("intent") in ["nlu_fallback", "out_of_scope"]
            coverage = 0 if is_fallback else 1
            
            # 1. Log response time asli (seperti sebelumnya)
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    tracker.sender_id,
                    user_event.get('text', ''),
                    user_event.get('intent', ''),
                    user_event.get('confidence', 0),
                    bot_event.get('text', ''),
                    f"{total_response_time:.2f}",
                    coverage
                ])
            
            # 2. Log confidence scores untuk semua intent
            self._log_confidence_scores(tracker, user_event)
            
            # 3. Log pipeline debug information
            self._log_pipeline_debug(tracker, user_event)