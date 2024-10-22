sanitized_json_sensor = """
create or replace view sanitized_json_sensor as (select
					replace(
						replace(
							replace(
								replace(
									replace(
										replace(
											replace(
												replace(
													replace(
															replace(
																replace(raw_json.json::text, '\\', ''), 
															'"v"', 'v'), 
													'"v1"', 'v1'),
												'"v2"', 'v2'),
											'"v3"','v3'),
										'"v4"','v4'),
									'"v5"','v5'),
								'"v6"','v6'),
							'"pm"','pm'),
						'"lastModified"','lastModified'),
				'"timeSinceModified"', 'timeSinceModified')::json as json from raw_json);
"""