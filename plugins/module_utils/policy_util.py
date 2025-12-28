import functools
from os import curdir
from pathlib import PurePosixPath
from qrexec.policy.admin_client import PolicyClient
import qrexec.tools.qubes_policy_lint as linter
import qrexec.tools.qubes_policy_editor as editor
from ansible_collections.bcduggan.qubes_aux.plugins.module_utils.tool_context import ToolContext, ToolContextError

class PolicyUtilError(Exception):
  pass

class PolicyUtilClientMethodError(PolicyUtilError):
  def __init__(self, method_name, *args, **kwargs):
    super().__init__(f"Error during client method '{method_name}'", *args, **kwargs)

class PolicyUtilNameValidationError(PolicyUtilError):
  def __init__(self, name, *args, **kwargs):
    super().__init__(f"Name validation failed for '{name}'", *args, **kwargs)

class PolicyUtilLintError(PolicyUtilError):
  def __init__(self, name, *args, **kwargs):
    super().__init__(f"Lint failed for '{name}'", *args, **kwargs)

class PolicyUtilParentValidationError(PolicyUtilError):
  def __init__(self, include_parent_path, parent_path, *args, **kwargs):
    super().__init__(f"Parent validation failed for '{parent_path}' != '{include_parent_path}'", *args, **kwargs)

def client_tool(func, *args, **kwargs):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    try:
      with ToolContext():
        return func(*args, **kwargs)
    except ToolContextError as exc:
      raise PolicyUtilClientMethodError(func.__name__) from exc
  return wrapper

class PolicyUtil:
  parent_path = PurePosixPath(curdir)
  include_parent_path = PurePosixPath(u"include")

  def __init__(self, name: str):
    try:
      with ToolContext():
        self.name = editor.validate_name(PurePosixPath(name).name)
    except ToolContextError as exc:
      raise PolicyUtilNameValidationError(self.name) from exc

    parent_path = PurePosixPath(name).parent

    if parent_path == self.include_parent_path:
      self.is_include = True
    elif parent_path == self.parent_path:
      self.is_include = False
    else:
      raise PolicyUtilParentValidationError(self.include_parent_path, parent_path)

    self.client = PolicyClient()

  def lint(self, content: str) -> None:
    try:
      with ToolContext(content):
        linter.parse_file("-", show=True, include_service=self.is_include)
    except ToolContextError as exc:
      raise PolicyUtilLintError(self.name) from exc

  def _client_method(self, method_name, *args, **kwargs):
    function_name = (
      "policy_include_"+method_name
      if self.is_include
      else "policy_"+method_name
    )
    method = getattr(self.client, function_name)
    return method(*args, **kwargs)

  @client_tool
  def get(self) -> tuple[str, str]:
    return self._client_method("get", self.name)

  @client_tool
  def remove(self) -> None:
    return self._client_method("remove", self.name)
  
  @client_tool
  def replace(self, content: str, token: str) -> None:
    return self._client_method("replace", self.name, content, token)

  @client_tool
  def list(self) -> list[str]:
    return self._client_method("list")
