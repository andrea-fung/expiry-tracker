from crewai import Agent, Crew, Process, Task, LLM
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from cert_tracker.crews.cert_tracker_crew.models import DataReport


@CrewBase
class ExtractionCrew:

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm_1b = LLM(model="ollama/qwen3:1.7b", base_url="http://localhost:11434")
    llm_9b = LLM(model="ollama/qwen3.5:9b", base_url="http://localhost:11434")

    @agent
    def extractor_agent(self) -> Agent:
        return Agent(config=self.agents_config['extractor_agent'],
                        llm=self.llm_9b)

    @task
    def data_extraction_task(self) -> Task:
        return Task(config=self.tasks_config['lead_data_extraction'],
                                agent=self.extractor_agent(),
                            output_pydantic=DataReport)
    @crew
    def extraction_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
