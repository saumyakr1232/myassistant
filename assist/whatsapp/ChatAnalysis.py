import io
from flashtext import KeywordProcessor

from assist.alert import NotifyMe


def get_messages():
	with io.open("../../data/messages.txt", 'r') as f:
		st = f.read()
	return st


def look_for_imp_messages(message_string, keyword_sets):
	"""
	:param message_string: Line of text where we will search for keywords
	:param keyword_sets: list of list of keywords
	:return: keywords_extracted (list(str)): List of terms/keywords found in sentence that match our corpus
	"""

	kp = KeywordProcessor()
	for keyword_set in keyword_sets:
		kp.add_keywords_from_list(keyword_set)

	return kp.extract_keywords(message_string, span_info=True)


class KeywordSets:
	KeyWordsSet0 = ['book', 'module', 'solution', 'answer', 'notes', 'pdf', 'video', 'result', 'list', 'notice', ]
	keyWordsSet1 = ['theory', 'lecture', 'class', 'lab', 'session', 'practical', ]
	keyWordsSet2 = ['quiz', 'assignment', ]
	keyWordsSet3 = ['lms', 'rf', 'gulms', 'gurf', 'inpods']
	keyWordsSet4 = ['survey', 'feedback', ]
	keyWordsSet5 = ['vc', 'vc mam', 'mam', 'sir', 'dean', 'dean sir', ]

	keyWordsSet6 = ['present', 'absent', 'attendance', ]
	keyWordsSet7 = ['exam', 'Exam', 'ete', 'mte', 'examination', 'examinations', 'debard', 'detain', 're-appear',
					're-mte',
					'debarred', 'detained', 'backpaper', 'test', 'paper', 'mid-term', 'mid term', 'end term',
					'end-term', 'mandatory', ]
	KeyWordsSet8 = ['workshop', 'webinar', 'event', 'competition', 'hakathon', ]

	keyWords = ['date', 'time', 'asap', 'timing', 'today', 'before', 'after', 'soon', ]
	actionsKeyWordsSet = ['fill', 'attempt', 'response', 'attend', 'join', 'watch', 'conduct', 'request', 'share',
						  'accept', ]
	vipKeywords = ['saumya']


class Action:
	@staticmethod
	def notification(keywords, group):
		for keyword in keywords:
			if keyword[0] == 'quiz':
				message = f"SomeOne Mention \"Quiz\" in {group}"
				NotifyMe.send_notification("Quiz Alert", message, NotifyMe.ICONS['danger'])
			elif keyword[0] == "assignment":
				pass

	@staticmethod
	def msg_box(keywords, group):
		for keyword in keywords:
			if keyword[0] == 'quiz':
				message = f"SomeOne Mention \"Quiz\" in {group}"
				result = NotifyMe.msg_box("Quiz Alert", message, 3)
				print(result)
			elif keyword[0] == "assignment":
				pass

	@staticmethod
	def voice_alert(keywords, group):
		for keyword in keywords:
			if keyword[0] == 'quiz':
				message = f"SomeOne Mention \"Quiz\" in {group}"
				NotifyMe.playSound(message)
			elif keyword[0] == "assignment":
				pass


def analyseMessageAndTakeAction(group, keyword_set_list, action):
	print("called : anatakeaction")
	previous_in_message = None
	last_in_message = get_messages()
	if last_in_message != previous_in_message:
		print(last_in_message)
		previous_in_message = last_in_message


if __name__ == '__main__':
	analyseMessageAndTakeAction("group", [KeywordSets.keyWordsSet2], Action.voice_alert)
