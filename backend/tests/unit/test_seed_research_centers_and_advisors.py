from scripts.seed_research_centers_and_advisors import build_advisor_seeds, build_center_seeds


def test_build_center_seeds_includes_director_and_deduplicates_advisors() -> None:
    seeds = build_center_seeds()
    frontier_center = next(item for item in seeds if item.center_name == "前沿探索中心")

    assert frontier_center.advisor_names[0] == "乔宇"
    assert frontier_center.advisor_names.count("乔宇") == 1
    assert "张超" in frontier_center.advisor_names


def test_build_advisor_seeds_uses_expected_pinyin_usernames_for_polyphonic_names() -> None:
    advisor_seeds = {item.full_name: item for item in build_advisor_seeds(build_center_seeds())}

    assert advisor_seeds["王潚崧"].username == "wangsusong"
    assert advisor_seeds["翟少鹏"].username == "dishaopeng"
    assert advisor_seeds["翟广涛"].username == "diguangtao"
    assert advisor_seeds["欧阳万里"].username == "ouyangwanli"
