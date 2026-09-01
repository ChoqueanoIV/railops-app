import { spawnSync } from 'node:child_process';
import { delimiter, dirname, join } from 'node:path';

const raiz = join(import.meta.dirname, '..', '..', '..');
const compose = join(raiz, 'compose.e2e.yaml');
const argumentosPlaywright = process.argv.slice(2);

function dockerExecutaveis() {
  if (process.env.DOCKER_BIN) return [process.env.DOCKER_BIN];

  const candidatos = ['docker'];
  if (process.platform === 'win32') {
    if (process.env.LOCALAPPDATA) {
      candidatos.push(
        join(
          process.env.LOCALAPPDATA,
          'Programs',
          'DockerDesktop',
          'resources',
          'bin',
          'docker.exe',
        ),
      );
    }
    if (process.env.ProgramFiles) {
      candidatos.push(
        join(
          process.env.ProgramFiles,
          'Docker',
          'Docker',
          'resources',
          'bin',
          'docker.exe',
        ),
      );
    }
  }
  return candidatos;
}

const candidatosDocker = dockerExecutaveis();

function executar(comando, args, opcoes = {}) {
  const resultado = spawnSync(comando, args, {
    cwd: raiz,
    encoding: 'utf8',
    stdio: 'inherit',
    ...opcoes,
  });
  if (resultado.error) throw resultado.error;
  if (resultado.status !== 0) {
    throw new Error(`${comando} terminou com código ${resultado.status}.`);
  }
}

function executarDocker(args) {
  let ultimoErro;
  for (const candidato of candidatosDocker) {
    try {
      const pastaDocker =
        candidato === 'docker' ? undefined : dirname(candidato);
      executar(candidato, args, {
        env: pastaDocker
          ? {
              ...process.env,
              PATH: `${pastaDocker}${delimiter}${process.env.PATH ?? ''}`,
            }
          : process.env,
      });
      return;
    } catch (erro) {
      if (
        !(erro instanceof Error) ||
        !('code' in erro) ||
        erro.code !== 'ENOENT'
      ) {
        throw erro;
      }
      ultimoErro = erro;
    }
  }
  throw ultimoErro ?? new Error('Docker não encontrado.');
}

let codigoSaida = 0;
try {
  executarDocker(['compose', '-f', compose, 'up', '--build', '--wait']);
  executarDocker([
    'compose',
    '-f',
    compose,
    '--profile',
    'tools',
    'run',
    '--rm',
    'seed',
  ]);
  executar(
    process.execPath,
    [
      join(raiz, 'frontend', 'react', 'node_modules', 'playwright', 'cli.js'),
      'test',
      ...argumentosPlaywright,
    ],
    { cwd: join(raiz, 'frontend', 'react') },
  );
} catch (erro) {
  codigoSaida = 1;
  console.error(erro instanceof Error ? erro.message : erro);
} finally {
  try {
    executarDocker(['compose', '-f', compose, 'down', '--volumes']);
  } catch (erro) {
    codigoSaida = 1;
    console.error('Não foi possível remover o ambiente E2E isolado.', erro);
  }
}

process.exitCode = codigoSaida;
