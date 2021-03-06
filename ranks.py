# -*- coding: utf-8 -*-

from semesters import get_current_semester, semester_date
from models import Mission, BridgeCrew

RANKS = [
		{
			# 0
			'name': 'Cadet',
			'abbr': 'Cdt.',
			'disp': ''
		}, {
			# 1
			'name': 'Ensign',
			'abbr': 'Ens.',
			'disp': unichr(9679) # ●
		}, {
			# 2
			'name': 'Lieutenant, Junior Grade',
			'abbr': 'Lt. J.G.',
			'disp': unichr(9675) + unichr(9679) # ○●
		}, {
			# 3
			'name': 'Lieutenant',
			'abbr': 'Lt.',
			'disp': unichr(9679) + unichr(9679) # ●●
		}, {
			# 4
			'name': 'Lieutenant Commander',
			'abbr': 'Lt. Cmdr.',
			'disp': unichr(9675) + unichr(9679) + unichr(9679) # ○●●
		}, {
			# 5
			'name': 'Commander',
			'abbr': 'Cmdr.',
			'disp': unichr(9679) + unichr(9679) + unichr(9679) # ●●●
		}, {
			# 6
			'name': 'Captain',
			'abbr': 'Capt.',
			'disp': unichr(9679) + unichr(9679) + unichr(9679) + unichr(9679) # ●●●●
		}, {
			# 7
			'name': 'Commodore',
			'abbr': 'Cmdre.',
			'disp': '[' + unichr(9679) + ']' # [●]
		}, {
			# 8
			'name': 'Rear Admiral',
			'abbr': 'Adm.',
			'disp': '[' + unichr(9679) + unichr(9679) + ']' # [●●]
		}, {
			# 9
			'name': 'Vice Admiral',
			'abbr': 'Adm.',
			'disp': '[' + unichr(9679) + unichr(9679) + unichr(9679) + ']' # [●●●]
		}, {
			# 10
			'name': 'Admiral',
			'abbr': 'Adm.',
			'disp': '[' + unichr(9679) + unichr(9679) + unichr(9679) + unichr(9679) + ']' # [●●●●]
		}, {
			# 11
			'name': 'Fleet Admiral',
			'abbr': 'Adm.',
			'disp': '[' + unichr(9679) + unichr(9679) + unichr(9679) + unichr(9679) + unichr(9679) + ']' # [●●●●●]
		}
	]

def rank(member, semester=get_current_semester()):
	paid = False
	num_semesters_paid_to_date = 0
	for semester_paid in member.semesters_paid:
		if semester_paid <= semester:
			paid = True
		if semester_paid < semester:
			num_semesters_paid_to_date += 1
	
	# Cadets cannot earn ranks
	if not paid:
		return 0
	
	rank = 1
	
	# Longevity
	if num_semesters_paid_to_date >= 4:
		rank += 1
	
	# Led weekly mission
	if Mission.query(Mission.runners == member.id, Mission.type == 0, Mission.start < semester_date(semester)).count(limit=1) != 0:
		rank += 1
	
	# Volunteered with special mission or committee
	if member.committee_rank or Mission.query(Mission.runners == member.id, Mission.type == 1, Mission.start < semester_date(semester)).count(limit=1) != 0:
		rank += 1
	
	# Merit ranks
	if member.merit_rank1:
		rank += 1
	if member.merit_rank2:
		rank += 1
	
	# Voted captain
	if BridgeCrew.query(BridgeCrew.captain == member.id, BridgeCrew.start < semester_date(semester)).count(limit=1) != 0:
		rank = 6
	
	# Alumni ranks
	if not member.current_student:
		if rank == 6:
			# Captains become rear admirals
			rank = 8
		else:
			# Non-captains become commodores
			rank = 7
	
	# Was an admiral (advisor)
	if BridgeCrew.query(BridgeCrew.admiral == member.id, BridgeCrew.start < semester_date(semester)).count(limit=1) != 0:
		rank = 10
	
	return rank

def rank_disp(member, semester=get_current_semester()):
	return RANKS[rank(member, semester)]['disp']

def rank_name(member, semester=get_current_semester()):
	return RANKS[rank(member, semester)]['name']

def name_with_rank(member, semester=get_current_semester()):
	return RANKS[rank(member, semester)]['abbr'] + ' ' + member.name
