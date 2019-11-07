from db import Doc
import sys


# interface for operating the mongodb data

# create or update
def create_or_update(intent,content):
	Doc.create_doc(intent,content)

# find
def find(intent):
	if(Doc.objects(topic=intent)):
		return Doc.objects(topic=intent)[0].content
	else:
		return "sorry, I don't know that."

# delete
def delete(intent):
	if(Doc.objects(topic=intent)):
		return Doc.objects(topic=intent).delete()
	return

# get intent list
def getIntentList():
	intentList = []
	for i in Doc.objects:
		intentList.append(i.topic)
	#print(intentList)
	return intentList

# ----------------for test--------------------
if __name__ == '__main__':
	# add record
	# create_or_update("Positive integers".lower(),"P = {1, 2, . . .}")
	# create_or_update("Integers".lower(),"Z = {. . . , −n, −(n − 1), . . . , −1, 0, 1, 2, . . .}")
	# create_or_update("fractions".lower(),"Q = { m/n: m,n ∈ Z, n != 0 }")
	# create_or_update("Union".lower(),"A ∪ B")
	# create_or_update("Intersection".lower(),"A ∩ B")
	# create_or_update("difference".lower(),"A \\ B,set difference, relative complement. It corresponds (logically) to a but not b")
	# create_or_update("symmetric difference".lower(),"A ⊕ B, A ⊕ B def= (A \\ B) ∪ (B \\ A) ")
	# create_or_update("complement".lower(),"")
	# create_or_update("Commutativity".lower(),"A ∪ B = B ∪ A, A ∩ B = B ∩ A")
	# create_or_update("Associativity".lower(),"(A ∪ B) ∪ C = A ∪ (B ∪ C ), (A ∩ B) ∩ C = A ∩ (B ∩ C )")
	# create_or_update("Distribution".lower(),"A ∪ (B ∩ C ) = (A ∪ B) ∩ (A ∪ C ), A ∩ (B ∪ C ) = (A ∩ B) ∪ (A ∩ C )")
	# create_or_update("Idempotence".lower(),"A ∪ A = A, A ∩ A = A")
	# create_or_update("Double Complementation".lower(),"(A c ) c = A")
	# create_or_update("De Morgan laws".lower(),"(A ∪ B) c = A c ∩ B c, (A ∩ B) c = A c ∪ B c")
	# create_or_update("proof".lower(),"A mathematical proof of a proposition p is a chain of logical deductions leading to p from a base set of axioms.")
	# create_or_update("logically equivalent".lower(),"Two formulas φ, ψ are logically equivalent, denoted φ ≡ ψ if they have the same truth value for all values of their basic propositions.")
	# create_or_update("satisfiable".lower(),"if a formula evaluates to T for some assignment of truth values to its basic propositions.")

		
	# create or update records
	if (len(sys.argv) == 3):
		create_or_update(sys.argv[1],sys.argv[2])
		print("create success: {},{}".format(sys.argv[1],sys.argv[2]))
	# delete records
	elif (len(sys.argv) == 2):
		delete(sys.argv[1])
		print("delete success: {}".format(sys.argv[1]))
	# show the records
	# print out the usage 	
	else:
		for i in Doc.objects:
			print("topic:",i.topic,"\ncontent:",i.content,"\njson format:",i,'\n')	
		print("this is the intent list:",getIntentList())

		print("\nusage:\n  create or update records: \tpython3 manager.py topic content")
		print("  show records: \tpython3 manager.py")
		print("  delete records: \tpython3 manager.py topic")
		pass

		sys.exit()





