import re
import asyncio
from typing import ClassVar
from metagpt. actions import Action
from metagpt. roles import Role
from metagpt. schema import Message
from metagpt. logs import logger

class SimpleCoder(Role):
    # def __init__(
    # self,
    # name: str = "Alice",
    # profile: str = "SimpleCoder",
    # **kwargs,
    # ):
    #     # super().__init__(name, profile, **kwargs)
    #     # 初始化父类，只传递 actions 参数
    #     super().__init__(actions=[SimpleWriteCode], **kwargs)
    #     # 单独设置 name 和 profile
    #     self.name = name
    #     self.profile = profile
    #     self._init_actions([SimpleWriteCode])
    name: str = "Alice"
    profile: str = "SimpleCoder"
    goal: str = "to write code"
    
    def __init__(self, **data):
        super().__init__(**data)
        self.set_actions([SimpleWriteCode])

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self.rc.todo}")
        todo = self.rc.todo # todo will be SimpleWriteCode()

        msg = self.get_memories(k=1)[0] # find the most recent messages

        code_text = await todo.run(msg. content)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))

        return msg
    

class SimpleWriteCode(Action):

    PROMPT_TEMPLATE: ClassVar[str] = """
    Write a python function that can {instruction} and provide two runnnable test cases.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """

    # def __init__(self, name="SimpleWriteCode", context=None, llm=None):
    #     super() .__init__(name, context, llm)

    async def run(self, instruction: str):

        prompt = self. PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)

        code_text = SimpleWriteCode.parse_code(rsp)
        
        return code_text
    
    @staticmethod
    def parse_code(rsp) :
        pattern = r'```python(.*)```'
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match. group(1) if match else rsp
        return code_text
    
async def main():
    msg = "write a function that calculates the sum of a list"
    role = SimpleCoder()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)

if __name__ == "__main__":
    asyncio.run(main())