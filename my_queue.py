class MyQueue:
	q = []

	def __init__(self, length:int=100):
		if length:
			self.length = length

	def push_q(self, elem: int) -> int:
		if self.is_peek():
			# print("Queue is maximum!!")
			_ = self.pop_q()
			self.q.append(elem)
		else:
			self.q.append(elem)
		return self.q

	def pop_q(self) -> int:
		try:
			self.q.remove(self.q[0])

			if self.is_empty():
				# print("Queue is empty!!")
				pass
		except IndexError:
			# print("Can't remove because Queue is empty!!")
			pass
		finally:
			return self.q

	def remove_all(self) -> None:
		self.q.clear()

	def top_q(self) -> int:
		return self.q[0]

	def is_empty(self) -> bool:
		return len(self.q) == 0

	def is_peek(self) -> bool:
		return len(self.q) > (self.length - 1)