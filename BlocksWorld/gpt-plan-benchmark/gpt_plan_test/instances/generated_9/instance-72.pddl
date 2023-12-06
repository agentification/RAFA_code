

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b d)
(ontable c)
(ontable d)
(on e i)
(on f c)
(on g e)
(ontable h)
(on i b)
(clear a)
(clear f)
(clear g)
)
(:goal
(and
(on a d)
(on c a)
(on d g)
(on f h)
(on g e)
(on i b))
)
)


