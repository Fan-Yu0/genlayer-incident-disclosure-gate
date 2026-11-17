import json

from conftest import to_hex

INCIDENT = "inc-2026-014"
URL = "https://vendor.example.com/security/inc-2026-014"
ALL = 31
CRITICAL = 2 | 8

BODY = (
    "Incident INC-2026-014. On 2026-10-01 we detected an exposed staging key. "
    "Root cause: the key was committed to a public mirror. "
    "Affected: staging API only, no production data. "
    "Remediation: key rotated, mirror purged, scanning added. "
    "Contact: security@vendor.example.com, CVE-2026-12345."
)


def _mock(vm, body=BODY, finding=None):
    vm.mock_web(r".*vendor\.example\.com/security/inc-2026-014.*", {"status": 200, "body": body})
    if finding is not None:
        vm.mock_llm(r".*INCIDENT DISCLOSURE SCREEN.*", json.dumps(finding))


def _finding(sections=None, days=3, consistency="consistent", summary="Complete disclosure."):
    return {
        "sections": sections
        if sections is not None
        else {
            "timeline": True,
            "root_cause": True,
            "affected_scope": True,
            "remediation": True,
            "contact": True,
        },
        "disclosure_days": days,
        "consistency": consistency,
        "summary": summary,
    }


def _register(contract, vm, publisher, required=ALL, max_days=30):
    vm.sender = publisher
    contract.register_incident(INCIDENT, "Vendor Inc", URL, required, max_days)


def _assess(contract, vm, publisher=INCIDENT):
    contract.assess(INCIDENT)


def test_complete_disclosure_is_approved(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock(direct_vm, finding=_finding())

    contract.assess(INCIDENT)

    result = contract.get_assessment(INCIDENT)
    assert result["state"] == 1
    assert result["decision"] == 1
    assert result["sections"] == ALL
    assert result["missing_sections"] == 0
    assert result["disclosure_days"] == 3
    assert result["within_sla"] is True
    assert contract.is_compliant(INCIDENT) is True


def test_missing_critical_section_is_blocked(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock(direct_vm, finding=_finding(sections={
        "timeline": True, "root_cause": True, "affected_scope": True,
        "remediation": False, "contact": True,
    }))

    contract.assess(INCIDENT)

    result = contract.get_assessment(INCIDENT)
    assert result["decision"] == 3
    assert result["missing_sections"] == 8
    assert contract.is_compliant(INCIDENT) is False


def test_missing_optional_section_is_conditional(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock(direct_vm, finding=_finding(sections={
        "timeline": True, "root_cause": True, "affected_scope": True,
        "remediation": True, "contact": False,
    }))

    contract.assess(INCIDENT)

    result = contract.get_assessment(INCIDENT)
    assert result["decision"] == 2
    assert result["missing_sections"] == 16


def test_late_disclosure_is_conditional(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice, max_days=7)
    _mock(direct_vm, finding=_finding(days=45))

    contract.assess(INCIDENT)

    result = contract.get_assessment(INCIDENT)
    assert result["decision"] == 2
    assert result["within_sla"] is False
    assert result["disclosure_days"] == 45


def test_conflicting_dates_need_review(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock(direct_vm, finding=_finding(consistency="conflicting"))

    contract.assess(INCIDENT)

    result = contract.get_assessment(INCIDENT)
    assert result["decision"] == 4
    assert result["consistency"] == "conflicting"


def test_unreadable_disclosure_needs_review(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice)
    direct_vm.mock_web(r".*vendor\.example\.com.*", {"status": 500, "body": ""})

    contract.assess(INCIDENT)

    result = contract.get_assessment(INCIDENT)
    assert result["decision"] == 4
    assert result["sections"] == 0


def test_duplicate_registration_is_rejected(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    try:
        contract.register_incident(INCIDENT, "Other Vendor", URL, ALL, 30)
        raised = False
    except Exception:
        raised = True
    assert raised is True


def test_empty_requirements_are_rejected(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    direct_vm.sender = direct_alice
    try:
        contract.register_incident(INCIDENT, "Vendor Inc", URL, 0, 30)
        raised = False
    except Exception:
        raised = True
    assert raised is True


def test_only_publisher_can_withdraw(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    _register(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    try:
        contract.withdraw(INCIDENT)
        raised = False
    except Exception:
        raised = True
    assert raised is True


def test_section_bits_are_stable(direct_deploy):
    contract = direct_deploy("contracts/incident_disclosure_gate.py")
    bits = contract.section_bits()
    assert bits["timeline"] == 1
    assert bits["root_cause"] == 2
    assert bits["affected_scope"] == 4
    assert bits["remediation"] == 8
    assert bits["contact"] == 16
    assert bits["all"] == 31
    assert bits["critical"] == 10
