from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

## Load environment variables ##
import os
from dotenv import load_dotenv
load_dotenv(".env")

## Load tools ##
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  TXTSearchTool,
  SerperDevTool,
  PDFSearchTool
)
from src.postulator.tools.custom_tool import human_feedback, ask_human, final_response_cleaner, letter_writer, PdfReaderTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_file = FileReadTool()
read_resume = FileReadTool(file_path='input/extended_resume.md')
#read_motivation_letter_example = FileReadTool(file_path='input/example_motivation_letter.tex')
#read_motivation_letter_example = FileReadTool(file_path='input/example_motivation.json')
read_motivation_letter_example = FileReadTool(file_path='input/example_motivation_letter.txt')
read_resume_template = FileReadTool(file_path='input/resume_template.tex')

response_cleaner_md = final_response_cleaner(strings_to_remove=["```md", "```markdown", "```", "'''md", "'''markdown", "'''"], result_as_answer=True)
response_cleaner_tex = final_response_cleaner(strings_to_remove=["```tex", "```", "'''tex", "'''"], result_as_answer=True)

read_pdf = PdfReaderTool()

semantic_search_pdf = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemini/gemini-1.5-flash",
				api_key=os.environ["GEMINI_API_KEY"],
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)

#"""
semantic_search_resume = MDXSearchTool(
	mdx='input/extended_resume.md',
	config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemini/gemini-1.5-flash",
				api_key=os.environ["GEMINI_API_KEY"],
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)
#"""

"""
semantic_search_resume = TXTSearchTool(
	txt = 'input/resume.tex',
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemini/gemini-1.5-flash",
				api_key=os.environ["GEMINI_API_KEY"],
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)
"""

# Initialize our model with zero temperature
gemini_flash_llm = LLM(
					model=os.environ["MODEL"], 
					api_key=os.environ["GEMINI_API_KEY"],
					temperature=0.0,
					)

@CrewBase
class Postulator():
	"""Postulator crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools = [scrape_tool, search_tool, read_file, read_pdf],#,semantic_search_pdf],
			verbose=True,
			llm = gemini_flash_llm,
			max_retry_limit=10
		)

	"""@agent
	def profiler(self) -> Agent:
		return Agent(
			config=self.agents_config['profiler'],
			tools = [#scrape_tool, search_tool,
             read_resume, semantic_search_resume],
			verbose=True,
			llm = gemini_flash_llm,
			max_retry_limit=10
		)"""
	
	@agent
	def profile_matcher(self) -> Agent:
		return Agent(
			config=self.agents_config['profile_matcher'],
			tools = [#scrape_tool, search_tool,
             read_resume, semantic_search_resume],
			verbose=True,
			llm = gemini_flash_llm,
			max_retry_limit=10
		)
	
	@agent
	def resume_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['resume_strategist'],
			tools = [scrape_tool,
             		 read_resume, 
					 semantic_search_resume, 
					 read_resume_template,
					 response_cleaner_md,
					 ],
			verbose=True,
			llm = gemini_flash_llm,
			max_retry_limit=10
		)
	
	@agent
	def resume_converter(self) -> Agent:
		return Agent(
			config=self.agents_config['resume_converter'],
			tools = [read_resume_template],
			verbose=True,
			llm = gemini_flash_llm,
			max_retry_limit=10
		)
	
	@agent
	def motivation_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['motivation_specialist'],
			tools = [read_motivation_letter_example,
					 human_feedback(),
					 letter_writer(result_as_answer=True)],#,response_cleaner_tex],#,ask_human()],
			verbose=True,
			llm = gemini_flash_llm,
			max_retry_limit=10,
		)
	
	@agent
	def interview_preparer(self) -> Agent:
		return Agent(
			config=self.agents_config['interview_preparer'],
			tools = [scrape_tool, 
					 search_tool,
					 read_resume, 
					 semantic_search_resume, 
					 response_cleaner_md],
			verbose=True,
			llm = gemini_flash_llm,
			max_retry_limit=10
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			context=[],
			max_retries=10,
			#async_execution=True
		)
	
	"""
	@task
	def profile_task(self) -> Task:
		return Task(
			config=self.tasks_config['profile_task'],
			context=[],
			max_retries=10,
			#async_execution=True
		)
	"""
	
	@task
	def strength_weakness_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['strength_weakness_analysis_task'],
			context=[self.research_task()],
			max_retries=10,
			#async_execution=True
		)

	@task
	def resume_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['resume_strategy_task'],
			output_file="output/tailored_resume.md",
    		context=[self.research_task(), self.strength_weakness_analysis_task()],
			max_retries=10,
		)

	@task
	def resume_conversion(self) -> Task:
		return Task(
			config=self.tasks_config['resume_conversion'],
			output_file="output/tailored_resume.tex",#md",
    		context=[self.resume_strategy_task()],
			max_retries=10,
		)

	@task
	def motivation_letter_task(self) -> Task:
		return Task(
			config=self.tasks_config['motivation_letter_task'],
			output_file="output/motivation_letter.tex",
			#removed self.resume_strategy_task(),
    		context=[self.research_task(), self.resume_strategy_task(), self.strength_weakness_analysis_task()],
			max_retries=10,
			#human_input=True,
		)
	
	@task
	def interview_preparation_task(self) -> Task:
		return Task(
			config=self.tasks_config['interview_preparation_task'],
			output_file="output/interview_materials.md",
			#removed  self.profile_task(),
    		context=[self.research_task(), self.resume_strategy_task(), self.motivation_letter_task()],
			max_retries=10,
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the Postulator crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents= [ self.researcher(), 
					  self.profile_matcher(), 
					  self.resume_strategist(),
					  #self.resume_converter(),
					  self.motivation_specialist(),
					  self.interview_preparer() ],#self.agents, # Automatically created by the @agent decorator
			tasks= [self.research_task(),
		   			self.strength_weakness_analysis_task(),
					self.resume_strategy_task(),
					#self.resume_conversion(),
					self.motivation_letter_task(),
					self.interview_preparation_task(),],#self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			max_rpm=20,
			chat_llm="gemini/gemini-2.0-flash",
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
