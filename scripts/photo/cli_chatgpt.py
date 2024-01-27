# resource(s): https://www.youtube.com/watch?v=7p7kJvckrFE

import typer
from dotenv import load_dotenv
from typing import Optional
load_dotenv()
from openai import OpenAI

def start_interactive_chat(
      initial_text: Optional[str] = None,
      on_chat_end=None
):

    app = typer.Typer()
    openai_client = OpenAI()


    @app.command()
    def interactive_chat(
        text: Optional[str] = typer.Option(initial_text, "--text", "-t", help="Start with text"),
        temperature: float = typer.Option(0.7, help="Control Randomness. Defaults to 0.7"),
        max_tokens: int = typer.Option(
            150, help="Control length of response. Defaults to 150"
        ),
        model: str = typer.Option(
            "gpt-3.5-turbo", help="Control the model to use. Defaults to gpt-3.5-turbo"
        ),
    ):
        """Interactive CLI tool to chat with ChatGPT."""

        typer.echo(
            "Starting interactive chat with ChatGPT. Type 'exit' to end the session."
        )

        messages = []

        while True:
            if text:
                prompt = text
                text = None
            else:
                prompt = typer.prompt("You")

            messages.append({"role": "user", "content": prompt})
            if prompt == "exit":
                typer.echo("ChatGPT: Goodbye!")
                # print(messages[-2].content)
                if on_chat_end:
                    on_chat_end(messages[-2])

                return messages[-2]

            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            typer.echo(f'ChatGPT: {response.choices[0].message.content}')
            messages.append(response.choices[0].message)

    app()
