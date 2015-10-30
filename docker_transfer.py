#!/usr/bin/env python
import argparse
import os
import subprocess


def get_image_id(tagged_image_name):
    image_name, image_tag = split_tagged_image_name(tagged_image_name)

    cmd_docker_images = subprocess.Popen(
        ('docker', 'images'), 
        stdout=subprocess.PIPE)

    cmd_grep_image_name = subprocess.Popen(
        ('grep', image_name), 
        stdin=cmd_docker_images.stdout, 
        stdout=subprocess.PIPE)

    cmd_grep_image_tag = subprocess.Popen(
        ('grep', image_tag), 
        stdin=cmd_grep_image_name.stdout, 
        stdout=subprocess.PIPE)

    cmd_awk_image_id = subprocess.Popen(
        ('awk', '{print $3}'),
        stdin=cmd_grep_image_tag.stdout,
        stdout=subprocess.PIPE)

    result = cmd_awk_image_id.communicate()[0].replace('\n', '')

    return result


def docker_pull(tagged_image_name):
    cmd_docker_pull = subprocess.Popen(
        ('docker', 'pull', tagged_image_name), stdout=subprocess.PIPE)

    with cmd_docker_pull.stdout:
        for line in iter(cmd_docker_pull.stdout.readline, b''):
            print line,

    cmd_docker_pull.wait()



def docker_tag(image_id, tagged_image_name):
    cmd_docker_tag = subprocess.Popen(
        ('docker', 'tag', image_id, tagged_image_name), 
        stdout=subprocess.PIPE)

    result = cmd_docker_tag.communicate()[0]

    return result


def docker_push(tagged_image_name):
    cmd_docker_push = subprocess.Popen(
        ('docker', 'push', tagged_image_name), stdout=subprocess.PIPE)

    with cmd_docker_push.stdout:
        for line in iter(cmd_docker_push.stdout.readline, b''):
            print line,

    cmd_docker_push.wait()


def docker_remove_image(tagged_image_name):
    cmd_docker_remove = subprocess.Popen(
        ('docker', 'rmi', '-f', tagged_image_name), 
        stdout=subprocess.PIPE)


def split_tagged_image_name(tagged_image_name):
    """ foo/bar/image_name:tag -> (foo/bar/image_name, tag)
    """
    image_name, image_tag = tagged_image_name.rsplit(':')
    return image_name, image_tag


##############################################################################


def parse_args():
    """ setup and run command line parser
    """
    parser = argparse.ArgumentParser(description=main.__doc__)

    parser.add_argument(
        '--source-repo',
        action='store',
        dest='source_repo',
        help='hostname or ip of source docker repo')

    parser.add_argument(
        '--dest-repo',
        action='store',
        dest='dest_repo',
        help='hostname or ip of dest docker repo')

    parser.add_argument(
        '--image-names',
        required=True,
        action='store',
        nargs='+',
        dest='tagged_image_names',
        help='list of base tagged image names to transfer')

    result = parser.parse_args()

    return result


def main():
    """ Pull, retag, and transfer images between two Docker Trusted Repos
    """
    args = parse_args()

    for tagged_image_name in args.tagged_image_names:
        source_tagged_image_name = "{}/{}".format(
            args.source_repo, tagged_image_name)

        dest_tagged_image_name = "{}/{}".format(
            args.dest_repo, tagged_image_name)

        # pull image from source repo
        docker_pull(source_tagged_image_name)

        # get image id 
        image_id = get_image_id(source_tagged_image_name)

        # retag the image for push to destination repo
        docker_tag(image_id, dest_tagged_image_name)

        # push image to destination repo
        docker_push(dest_tagged_image_name)

if __name__ == '__main__':
    main()