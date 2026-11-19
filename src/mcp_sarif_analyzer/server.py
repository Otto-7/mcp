from fastmcp import FastMCP
import core
import argparse
from pathlib import Path
import config


mcp = FastMCP("Security Audit Server")

@mcp.tool()
def get_summary() -> dict:
    return core.get_summary() #общая сводка по ошибкам

@mcp.tool()
def get_results(
    severity: str | None = None,
    status: str | None = None,
    has_comment: bool | None = None,
    has_review: bool | None = None,
    rule_id: str | None = None,
    file: str | None = None,
    offset: int = 0,
    limit: int = 20) -> dict:
    return core.get_results(severity, status, has_comment, has_review, rule_id, file, offset, limit)

@mcp.tool()
def get_result(finding_id: str) -> dict:
    return core.get_result(finding_id)

@mcp.tool()
def get_rule(rule_id: str) -> dict: #описание правила
    return core.get_rule(rule_id)

@mcp.tool()
def save_reviews(records: list[dict]) -> dict:
    """Сохранить вердикты. Формат записи: {'finding_id': '...', 'verdict': '...', 'text': '...'}. Допустимые verdict: P0, P1, P2, NA, FP, Need_analysis."""
    return core.save_reviews(records)

@mcp.tool()
def export_sarif() -> dict:
    """Собрать итоговый SARIF-отчет с вердиктами LLM"""
    return core.export_sarif_report()

@mcp.prompt()
def full_audit() -> str:
    return (
        "Ты — опытный security-инженер, проводящий триаж уязвимостей по строгому регламенту.\n"
        "Твоя задача — проанализировать ошибки и присвоить им классы.\n\n"
        
        "КОНТЕКСТ (Поверхность атаки 1-го уровня):\n"
        "- Устройства: USB, USB HID, USB-token\n"
        "- Файловые системы, initramfs\n"
        "- GUI (вход в систему)\n"
        "- Контроль целостности (до загрузки ОС)\n\n"
        
        "ПРАВИЛА КЛАССИФИКАЦИИ:\n"
        "- P0: Блокирующее замечание. Код достижим, входные данные контролируются нарушителем, приводит к обходу И/А или загрузке ОС без проверки.\n"
        "- P1: Ошибка реальна, но P0 исключен (например, нет пути выполнения или не на поверхности атаки).\n"
        "- P2: Ошибка низкого риска.\n"
        "- NA (Not Applicable): Компонент/модуль отсутствует в конфигурации.\n"
        "- FP (False Positive): Ложное срабатывание.\n"
        "- Need_analysis: Недостаточно данных для исключения P0.\n\n"
        
        "ПОРЯДОК ДЕЙСТВИЙ:\n"
        "1. Вызови get_summary(), чтобы узнать количество ошибок (remaining).\n"
        "2. Пока remaining > 0, вызывай get_results(has_review=false, offset=0, limit=3).\n"
        "3. Для КАЖДОЙ ошибки из списка ОБЯЗАТЕЛЬНО вызови get_result(finding_id), чтобы прочитать полные данные: trace (путь выполнения) и comments (комментарии ревьюеров). Без этого вызова анализ будет неполным. Если нужно, вызови get_rule.\n"
        "4. Присвой вердикт (P0, P1, P2, NA, FP, Need_analysis).\n"
        "5. Сформируй комментарий СТРОГО по шаблону (см. ниже).\n"
        "6. Сохрани пачку через save_reviews().\n"
        "7. ВАЖНО: если после сохранения remaining не уменьшилось — остановись.\n"
        "8. Когда remaining станет 0, вызови export_sarif()\n\n"
        
        "ШАБЛОН КОММЕНТАРИЯ (поле text) для каждой ошибки:\n"
        "[6.1 <область>] <ID>: <подсистема>.\n"
        "Источник замечания: статический анализ.\n"
        "Ссылка / артефакт: <rule_id>.\n"
        "Базовая опасность: <severity>.\n"
        "Компонент: <имя>.\n"
        "Подсистема/путь выполнения: <краткое описание из trace>.\n"
        "Очередь: <A | B | C | D>.\n"
        "Применимость: <да | нет | частично | не подтверждено>, основание: <CONFIG | модуль | интерфейс>.\n"
        "Принадлежность к поверхности атаки: <на поверхности | вне поверхности | требуется уточнение>.\n"
        "Влияние: <обход И/А | подмена доверенного состояния | нарушение контроля целостности | только DoS | отсутствует>.\n"
        "Доказательство: <trace | отсутствие пути выполнения>.\n"
        "Компенсирующая мера: <не требуется | отсутствует | требуется уточнить>.\n\n"
        
        "Пиши заполненный шаблон в поле text. Будь строг и аргументирован."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sarif", type=str, default=config.DEFAULT_SARIF)
    args = parser.parse_args()
    config.SARIF_PATH = Path(args.sarif)
    mcp.run()
