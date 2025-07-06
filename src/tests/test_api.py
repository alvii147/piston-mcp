from unittest import IsolatedAsyncioTestCase

from piston_mcp.api import PistonClient


class TestPistonClient(IsolatedAsyncioTestCase):
    async def test_runtimes(self):
        async with PistonClient() as client:
            runtimes = await client.runtimes()

        self.assertGreater(len(runtimes), 0)

        python3_runtime = None
        for runtime in runtimes:
            if runtime['language'] == 'python':
                python3_runtime = runtime
                break

        self.assertIsNotNone(python3_runtime)
        self.assertIn('version', python3_runtime)
        self.assertIn('aliases', python3_runtime)

    async def test_execute(self):
        async with PistonClient() as client:
            results = await client.execute(
                'python',
                '3.10.0',
                [
                    {
                        'content': 'print(42)',
                    },
                ],
            )

        self.assertEqual(results['language'], 'python')
        self.assertEqual(results['version'], '3.10.0')
        self.assertEqual(results['run']['stdout'], '42\n')
        self.assertEqual(results['run']['stderr'], '')
        self.assertEqual(results['run']['output'], '42\n')
        self.assertEqual(results['run']['code'], 0)
        self.assertIsNone(results['run']['signal'])
