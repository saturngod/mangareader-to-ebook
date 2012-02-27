#!/usr/bin/env ruby

require 'rubygems'
require 'mechanize'
require 'fileutils'

BROWSER = Mechanize.new { |agent|  agent.user_agent_alias = "Mac Safari"}

def cleanup! dir_name
  include FileUtils
  files = Dir["#{dir_name}/*.jpg"]
  chapters = files.map { |f| f.split('/').last.split('Page').first.split('-').first.sub(/_$/,'') }.uniq

  puts "Moving pages into chapters\n #{chapters.join("\n\t")}"

  chapters.each do |chapter|
    dir = "#{dir_name}/#{chapter}"
    mkdir  dir unless File.exists?  dir
    files.select { |file| file =~ /#{chapter}_/ }.each do |_file|
      file = _file.split('/').last
      mv _file, "#{dir_name}/#{chapter}/#{file}"
    end

  end

end
def getit! dir_name, target_url
  puts ">>>> #{target_url}"

  begin
    BROWSER.get(target_url) do |page|
      next_url = "http://"
      next_url << page.uri.host
      next_url << page.search('.//div[@id="imgholder"]//a').attr('href').to_s

      url = page.search('.//div[@id="imgholder"]//img').attr('src').to_s

      name = (page.title.gsub(/[\ \/:]/, '_')+"."+url.split('.').last).gsub /[:\/]/,''

      name = name =~ /Page\_\d\.jpg/ ?  name.sub('Page_', 'Page_0') : name

      puts ">>>> Downloading #{name} ( #{url} )"

      pid = fork { `curl -s #{url} > #{dir_name}/#{name}` }
      Process.detach pid

      getit! dir_name, next_url
    end
  rescue => e
    puts "Failed at #{target_url} - probably we reached the end!"
    puts e.inspect unless ENV['DEBUG'].nil?
    puts 'cleaning up'
    cleanup! dir_name
    exit 1
  end
end

if ENV['CLEANUP'].nil?
  puts "usage: \nruby mdl.rb <DIR> '<STARTURL>'" and exit  1 if ARGV.length < 2
  getit! ARGV[0], ARGV[1]
else
  cleanup! ARGV[0]
end
