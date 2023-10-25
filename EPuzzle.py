from collections import deque


class EightPuzzleProblem:
    def __init__(self, initial_state, goal_state):
        self.initial = initial_state  # Trạng thái ban đầu của bài toán
        self.goal = goal_state  # Trạng thái mục tiêu của bài toán
        self.step_cost = 1  # Chi phí di chuyển giữa các trạng thái liên tiếp

    def Action(self, state):
        # Trả về các hành động có thể thực hiện dựa trên trạng thái hiện tại
        possible_action = {'UP', 'DOWN', 'RIGHT', 'LEFT'}
        blank_id = state.index(0)  # Xác định vị trí của ô trống

        if (blank_id % 3 == 0):
            possible_action.remove('LEFT')  # Nếu ô trống ở cột đầu tiên, không thể di chuyển sang trái
        if (blank_id % 3 == 2):
            possible_action.remove('RIGHT')
             # Nếu ô trống ở cột cuối, không thể di chuyển sang phải

        if (blank_id // 3 < 1):
            possible_action.remove('UP')  # Nếu ô trống ở hàng đầu, không thể di chuyển lên
        if (blank_id // 3 >= 2):
            possible_action.remove('DOWN')  # Nếu ô trống ở hàng cuối, không thể di chuyển xuống
        return possible_action

    def Result(self, state, action):
        # Trả về trạng thái mới sau khi thực hiện một hành động
        state = list(state)
        blank_id = state.index(0)
        if action == 'UP' and blank_id >= 3:
            state[blank_id], state[blank_id - 3] = state[blank_id - 3], state[blank_id]
        if action == 'DOWN':
            state[blank_id], state[blank_id + 3] = state[blank_id + 3], state[blank_id]
        if action == 'LEFT':
            state[blank_id], state[blank_id - 1] = state[blank_id - 1], state[blank_id]
        if action == 'RIGHT' and blank_id % 3 != 2:
            state[blank_id], state[blank_id + 1] = state[blank_id + 1], state[blank_id]
        return tuple(state)

    def Step_Cost(self, cur_state, nx_state):
        # Trả về chi phí di chuyển từ trạng thái hiện tại đến trạng thái mới
        return self.step_cost

    def Path_Cost(self, cur_state, cur_cost, nx_state):
        # Trả về chi phí tổng của một đường đi từ trạng thái ban đầu đến trạng thái hiện tại
        return cur_cost + self.Step_Cost(cur_state, nx_state)

    def Goal_test(self, state):
        # Kiểm tra xem trạng thái hiện tại có phải là trạng thái mục tiêu không
        return (state == self.goal)


class Node:
    def __init__(self, state, parent=None, action=None, cost=0, depth=0):
        self.state = state  # Trạng thái của nút
        self.parent = parent  # Nút cha của nút hiện tại
        self.action = action  # Hành động dẫn đến trạng thái hiện tại
        self.cost = cost  # Chi phí tích luỹ để đến nút hiện tại
        if parent:
            self.depth = depth  # Độ sâu của nút trong cây tìm kiếm
        else:
            self.depth = 0

    def child_Node(self, action, problem):
        # Trả về một nút con sau khi thực hiện một hành động
        new_state = problem.Result(self.state, action)
        new_cost = self.cost + problem.Step_Cost(self.state, new_state)
        return Node(new_state, self, action, new_cost, self.depth + 1)

    def Expand(self, possible_action, problem):
        # Mở rộng nút hiện tại để tạo ra các nút con
        List_successor = []
        for action in possible_action:
            List_successor.append(self.child_Node(action, problem))
        return List_successor

    def Solution(self):
        # Trả về lời giải (danh sách các hành động) từ nút gốc đến nút hiện tại
        node, solution = self, []
        while node.parent:
            solution.append(node.action)
            node = node.parent
        return list(reversed(solution))


class EightPuzzleSolving:
    def __init__(self, problem):
        self.solution = self.iterative_deepening_search(
            problem).Solution();  # Phải gọi phương thức và truy cập thuộc tính "solution" một cách chính xác.

    def recursive_DLS(self, node, problem, limit):
        if (problem.Goal_test(node.state)):
            return node
        if (limit == 0):
            return None
        list_child = node.Expand(problem.Action(node.state), problem)
        for child in list_child:
            result = self.recursive_DLS(child, problem, limit - 1)
            if (result):
                return result
        return None

    def Depth_limit_search(self, problem, limit):
        return self.recursive_DLS(Node(problem.initial, None, None, 0), problem, limit)

    def iterative_deepening_search(self, problem):
        for limit in range(0, 50):
            result = self.Depth_limit_search(problem, limit)
            if (result):
                return result


class OptimalSolutionChecker:
    def __init__(self, problem, solution):
        self.solution = self.breadth_first_graph_search(problem).Solution()
        self.isOptimal_solution = (self.solution == solution)

    def breadth_first_graph_search(self, problem):
        node = Node(problem.initial)
        if problem.Goal_test(node.state):
            return node
        frontier = deque([node])
        explored = set()
        while frontier:
            node = frontier.popleft()
            explored.add(node.state)
            for child in node.Expand(problem.Action(node.state), problem):
                if child.state not in explored and child not in frontier:
                    if problem.Goal_test(child.state):
                        return child
                frontier.append(child)


if __name__ == '__main__':
    import time

    problem = EightPuzzleProblem(initial_state=(3, 1, 2, 6, 0, 8, 7, 5, 4), goal_state=(0, 1, 2, 3, 4, 5, 6, 7, 8))
    solving = EightPuzzleSolving(problem)
    checker = OptimalSolutionChecker(problem, solving.solution)
    print("Solution:", solving.solution)
    print("Is Optimal Solution?", checker.solution)
    if(checker.isOptimal_solution):
        print("YES! OPTIMAL SOLUTION")
    else:
        print("NO! BAD SOLVING")
