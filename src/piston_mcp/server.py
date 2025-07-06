from mcp.server.fastmcp import FastMCP
from .api import PistonClient


mcp = FastMCP('piston')


@mcp.tool()
async def run_code(language: str, code: str) -> str:
    """
    Runs given code in the given language in the Piston remote code execution engine.

    Parameters
    ----------
    language: str
        Programming language to run code in.

    code : str
        Code to run.

    Return
    ------
    str
        Output of code execution.
    """
    client = PistonClient()

    # get runtimes
    try:
        runtimes_response = await client.runtimes()
    except Exception:
        return 'ERROR: failed to get runtimes.'

    language = language.lower()
    version = None

    # iterate over runtimes and find version for given language
    for runtime in runtimes_response:
        if 'version' not in runtime:
            continue

        if 'language' in runtime and runtime['language'] == language:
            version = runtime['version']
            break

        if 'aliases' in runtime and language in runtime['aliases']:
            version = runtime['version']
            break

    # if version is not found, then the language is not supported
    if version is None:
        return 'ERROR: invalid language.'

    # execute code using language and version
    try:
        execute_response = await client.execute(
            language=language,
            version=version,
            files=[
                {
                    'content': code,
                },
            ],
        )
    except Exception:
        return 'ERROR: failed to execute code.'

    output = execute_response.get('run', {}).get('output', '')

    return output


def main():
    mcp.run(transport='stdio')


if __name__ == '__main__':
    main()
