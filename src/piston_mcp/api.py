from typing import NamedTuple
import httpx


# publicly deployed Piston URL to use as default for getting runtimes
DEFAULT_RUNTIMES_URL = 'https://emkc.org/api/v2/piston/runtimes'
# publicly deployed Piston URL to use as default for executing code
DEFAULT_EXECUTE_URL = 'https://emkc.org/api/v2/piston/execute'


class Runtime(NamedTuple):
    """
    Runtime that can be executed.
    """

    language: str
    version: str
    aliases: list[str]


class File:
    """
    File that can be submitted in execute requests.
    """

    name: str | None
    content: str
    encoding: str | None


class ExecuteStageResults(NamedTuple):
    """
    Results on a particular stage on execute requests.
    """

    stdout: str
    stderr: str
    output: str
    code: int | None
    signal: str | None
    message: str | None
    status: str | None
    cpu_time: int | None
    wall_time: int | None
    memory: int | None


class ExecuteResults(NamedTuple):
    """
    Results on execute requests.
    """

    language: str
    version: str
    compile: ExecuteStageResults | None
    run: ExecuteStageResults


class PistonClient:
    """
    Client for interacting with the Piston API.

    For more information, visit https://github.com/engineer-man/piston.

    Parameters
    ----------
    runtimes_url : str, optional
        URL for runtimes requests (defaults to https://emkc.org/api/v2/piston/runtimes).

    execute_url : str, optional
        URL for execute requests (defaults to https://emkc.org/api/v2/piston/execute).

    timeout : float, optional
        Request timeout in seconds (defaults to 10 seconds).

    Attributes
    ----------
    runtimes_url : str
        URL for runtimes requests.

    execute_url : str
        URL for execute requests.

    client: httpx.AsyncClient
        HTTP client used for making asynchronous requests.
    """

    def __init__(
        self,
        runtimes_url: str = DEFAULT_RUNTIMES_URL,
        execute_url: str = DEFAULT_EXECUTE_URL,
        timeout: float = 10.0,
    ):
        self.runtimes_url = runtimes_url
        self.execute_url = execute_url
        self.client = httpx.AsyncClient(timeout=timeout)

    async def runtimes(self) -> list[Runtime]:
        """
        Get list of available runtimes.

        Returns
        -------
        list of Runtime
            List of available runtimes.
        """
        response = await self.client.get(url=self.runtimes_url)
        response.raise_for_status()

        return response.json()

    async def execute(
        self,
        language: str,
        version: str,
        files: list[File],
        stdin: str | None = None,
        args: list[str] | None = None,
        compile_timeout: int | None = None,
        run_timeout: int | None = None,
        compile_cpu_time: int | None = None,
        run_cpu_time: int | None = None,
        compile_memory_limit: int | None = None,
        run_memory_limit: int | None = None,
    ) -> ExecuteResults:
        """
        Execute code with the given language, version, and files.

        Parameters
        ----------
        language : str
            Programming language to use.

        version : str
            Version of language to use.

        files : list of File
            List of files to be executed. The first file is considered the main file.
            A file is represented by a dictionary, with its contents in the "content" key.
            Optionally, the dictionary may also include a "name" and an "encoding" scheme.
            There must be at least one file.

        stdin : str, optional
            Stdin to be passed to the program.

        args : list of str, optional
            Command-line arguments to be passed to the program.

        compile_timeout : int, optional
            Maximum wall-time allowed for the compile stage to finish in milliseconds.

        run_timeout : int, optional
            Maximum wall-time allowed for the run stage to finish in milliseconds.

        compile_cpu_time : int, optional
            Maximum CPU-time allowed for the compile stage to finish in milliseconds.

        run_cpu_time : int, optional
            Maximum CPU-time allowed for the run stage to finish in milliseconds.

        compile_memory_limit : int, optional
            Maximum amount of memory the compile stage is allowed to use in bytes.

        run_memory_limit : int, optional
            Maximum amount of memory the run stage is allowed to use in bytes.

        Returns
        -------
        ExecuteResults
            Results of the execution.
        """
        if len(files) < 1:
            raise ValueError('No files provided')

        validated_files = []
        for file in files:
            if 'content' not in file:
                raise ValueError('No content in file')

            validated_file = {
                'content': file['content'],
            }

            if 'name' in file:
                validated_file['name'] = file['name']

            if 'encoding' in file:
                validated_file['encoding'] = file['encoding']

            validated_files.append(validated_file)

        data = {
            'language': language,
            'version': version,
            'files': validated_files,
        }

        if stdin is not None:
            data['stdin'] = stdin

        if args is not None:
            data['args'] = args

        if compile_timeout is not None:
            data['compile_timeout'] = compile_timeout

        if run_timeout is not None:
            data['run_timeout'] = run_timeout

        if compile_cpu_time is not None:
            data['compile_cpu_time'] = compile_cpu_time

        if run_cpu_time is not None:
            data['run_cpu_time'] = run_cpu_time

        if compile_memory_limit is not None:
            data['compile_memory_limit'] = compile_memory_limit

        if run_memory_limit is not None:
            data['run_memory_limit'] = run_memory_limit

        response = await self.client.post(
            url=self.execute_url,
            json=data,
        )
        response.raise_for_status()

        return response.json()

    async def close(self):
        """
        Close the HTTP client.
        """
        await self.client.aclose()

    async def __aenter__(self):
        """
        Enter the async context manager.

        Returns
        -------
        PistonClient
            The client itself.
        """
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Exit the async context manager.

        Parameters
        ----------
        exc_type : Type[BaseException], optional
            Exception type, if any.

        exc : BaseException, optional
            Exception instance, if any.

        tb : TracebackType, optional
            Traceback, if any.
        """
        await self.close()
