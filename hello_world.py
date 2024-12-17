import dspy
import os

# Configurar el LM usando LiteLLM a través de DSPy
os.environ['OPENAI_API_KEY'] = 'YOUR_API_KEY'
lm = dspy.LM('openai/gpt-3.5-turbo')
dspy.configure(lm=lm)

# Definir una firma simple para nuestro hola mundo
class HelloWorld(dspy.Signature):
    """Generate a hello world message."""
    name = dspy.InputField()
    greeting = dspy.OutputField(desc="A friendly greeting message")

# Crear el módulo usando ChainOfThought
hello = dspy.ChainOfThought(HelloWorld)

# Llamar al predictor
result = hello(name="World")
print(result.greeting) 