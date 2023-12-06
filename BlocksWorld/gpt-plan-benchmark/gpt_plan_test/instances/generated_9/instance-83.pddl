

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a i)
(ontable b)
(on c f)
(ontable d)
(on e b)
(ontable f)
(ontable g)
(on h e)
(ontable i)
(clear a)
(clear c)
(clear d)
(clear g)
(clear h)
)
(:goal
(and
(on a b)
(on b g)
(on c d)
(on d a)
(on e h)
(on i f))
)
)


