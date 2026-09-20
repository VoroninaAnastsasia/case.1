import json
from dataclasses import asdict

import click

from application.use_cases import analyzeText, analyzeBatch


def resultToDict(result):
  """Превращает результат анализа в обычный словарь для вывода в JSON."""
  data = asdict(result)
  # Enum-значения превращаем в строки.
  if hasattr(data['language'], 'name'):
    data['language'] = data['language'].name
  if hasattr(data['polarity'], 'name'):
    data['polarity'] = data['polarity'].name
  return data


def printResult(result, sourceLabel=None):
  """Красиво выводит один результат в терминал."""
  data = resultToDict(result)

  if sourceLabel:
    click.echo(f'=== {sourceLabel} ===')

  click.echo(f"  Язык:              {data['language']}")
  click.echo(f"  Тональность:       {data['polarity']}")
  click.echo(f"  Субъективность:    {round(data['subjectivity'] * 100)}%")
  click.echo(f"  Читаемость:        {round(data['flesch_index'], 1)}")
  click.echo(f"  Уровень:           {round(data['flesch_kincaid'], 1)}")
  click.echo(f"  Разнообразие слов: {round(data['lexical_diversity'] * 100)}%")
  click.echo(f"  Слов:              {data['stats']['word_count']}")
  click.echo(f"  Предложений:       {data['stats']['sentence_count']}")
  click.echo(f"  Итог:              {data['interpretation']}")
  click.echo('')


@click.group()
def cli():
  """CLI для анализа текста."""
  pass


@cli.command()
@click.option('--text', 'text', default=None, help='Текст для анализа')
@click.option('--file', 'filePath', default=None, help='Путь к файлу с текстом')
@click.option('--batch-file', 'batchPath', default=None, help='Путь к файлу со списком текстов (по одному на строку)')
@click.option('--json', 'asJson', is_flag=True, help='Вывести результат как JSON')
def analyze(text, filePath, batchPath, asJson):
  """Анализирует текст из аргумента, файла или списка файлов."""

  # Проверяем, что задан ровно один источник.
  sourcesCount = sum(1 for x in [text, filePath, batchPath] if x is not None)
  if sourcesCount == 0:
    raise click.UsageError('Укажите --text, --file или --batch-file')
  if sourcesCount > 1:
    raise click.UsageError('Можно указать только один источник: --text, --file или --batch-file')

  # --- Анализ текста из аргумента ---
  if text is not None:
    result = analyzeText(text)
    if asJson:
      click.echo(json.dumps(resultToDict(result), ensure_ascii=False, indent=2))
    else:
      printResult(result)

  # --- Анализ текста из файла ---
  elif filePath is not None:
    try:
      with open(filePath, 'r', encoding='utf-8') as f:
        content = f.read()
    except FileNotFoundError:
      raise click.ClickException(f'Файл не найден: {filePath}')

    result = analyzeText(content)
    if asJson:
      click.echo(json.dumps(resultToDict(result), ensure_ascii=False, indent=2))
    else:
      printResult(result, sourceLabel=filePath)

  # --- Пакетный анализ ---
  elif batchPath is not None:
    try:
      with open(batchPath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
      raise click.ClickException(f'Файл не найден: {batchPath}')

    if not lines:
      raise click.ClickException('Файл пустой')

    results = analyzeBatch(lines)

    if asJson:
      output = [resultToDict(r) for r in results]
      click.echo(json.dumps(output, ensure_ascii=False, indent=2))
    else:
      for i, result in enumerate(results):
        printResult(result, sourceLabel=f'Текст #{i + 1}: {lines[i]}')


if __name__ == '__main__':
  cli()
